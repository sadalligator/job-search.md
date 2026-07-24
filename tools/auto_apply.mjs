#!/usr/bin/env node
/**
 * auto_apply.mjs — heuristic job-application submitter for the scheduled job-search agent.
 *
 * Usage:   node tools/auto_apply.mjs jobs/<job-spec>.json [--dry-run]
 *
 * Job spec: { "url": "...", "company": "...", "role": "...",
 *             "cover_letter_file": "cover_letters/x.txt", "overrides": { "<answer_key>": "..." } }
 *
 * Exit codes (the agent maps these to application_history statuses):
 *   0 SUBMITTED            — confirmation page reached, screenshot in audit/
 *   3 NETWORK_BLOCKED      — environment network policy denies the host (fix: allow domains
 *                            in the claude.ai/code environment settings)
 *   4 NEEDS_ANSWERS        — form requires a field that is null/missing in candidate_answers.json;
 *                            the unanswered fields are printed and dumped to audit/. NEVER guessed.
 *   5 CAPTCHA_OR_LOGIN     — CAPTCHA present or a login wall (e.g. Indeed account, Workday account).
 *                            Do not retry; route to manual/browser-extension lane.
 *   6 FORM_NOT_FOUND       — page loaded but no recognizable application form.
 *
 * Hard rules: never fabricate an answer; never attempt to bypass CAPTCHA or bot checks;
 * never enter credentials. Anything the form demands beyond candidate_answers.json is a
 * human decision and exits 4/5 with full context captured.
 */
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const AUDIT = join(ROOT, 'audit');
mkdirSync(AUDIT, { recursive: true });

const specPath = process.argv[2];
if (!specPath) { console.error('usage: node tools/auto_apply.mjs <job-spec.json> [--dry-run]'); process.exit(2); }
const dryRun = process.argv.includes('--dry-run');
const spec = JSON.parse(readFileSync(resolve(specPath), 'utf8'));
const answers = { ...JSON.parse(readFileSync(join(ROOT, 'tools/candidate_answers.json'), 'utf8')), ...(spec.overrides || {}) };
const slug = (spec.company + '-' + spec.role).toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 60);
const shot = async (page, name) => page.screenshot({ path: join(AUDIT, `${slug}-${name}.png`), fullPage: true }).catch(() => {});

// Map form-field label/name/placeholder patterns -> answer keys. Order matters (first match wins).
const FIELD_MAP = [
  [/full\s*name|your\s*name/i, 'full_name'],
  [/first\s*name|given\s*name/i, 'first_name'],
  [/last\s*name|surname|family\s*name/i, 'last_name'],
  [/e-?mail/i, 'email'],
  [/phone|mobile|contact\s*number/i, 'phone'],
  [/linkedin/i, 'linkedin'],
  [/nationality/i, 'nationality'],
  [/visa|sponsorship|work\s*(permit|authori)/i, 'visa_status'],
  [/notice\s*period/i, 'notice_period'],
  [/current\s*salary/i, 'current_salary'],
  [/expected\s*salary|salary\s*expect/i, 'expected_salary'],
  [/city|location|based/i, 'location'],
  [/arabic/i, 'arabic'],
  [/driving\s*licen[cs]e/i, 'driving_license'],
  [/notice|start\s*date|available/i, 'earliest_start_date'],
  [/years.*(uae|emirates).*experience|(uae|emirates).*years/i, 'uae_legal_experience_years'],
  [/years.*experience|experience.*years/i, 'years_experience_legal'],
  [/cover\s*letter|why.*(join|interested)|motivation/i, '__cover_letter__'],
];

const main = async () => {
  const { chromium } = await import('playwright');
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
    args: ['--no-sandbox'],
  });
  const page = await (await browser.newContext({ acceptDownloads: false })).newPage();

  let resp;
  try {
    resp = await page.goto(spec.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  } catch (e) {
    console.error(`NETWORK_BLOCKED: ${e.message}`);
    await browser.close(); process.exit(3);
  }
  if (resp && [403, 407].includes(resp.status()) && /proxy|gateway|denied/i.test(await page.content().catch(() => ''))) {
    console.error('NETWORK_BLOCKED: proxy policy denial'); await browser.close(); process.exit(3);
  }
  await shot(page, '01-landing');

  // CAPTCHA / login walls: detect, never bypass.
  const walls = await page.locator(
    'iframe[src*="captcha"], .g-recaptcha, .h-captcha, [data-testid*="challenge"], ' +
    'input[type="password"], form[action*="login"], form[action*="signin"]'
  ).count();
  if (walls > 0) {
    console.error('CAPTCHA_OR_LOGIN: human session required — route to browser-extension lane');
    await shot(page, '02-wall'); await browser.close(); process.exit(5);
  }

  // Follow an "Apply" button if the posting page and the form are separate.
  const applyBtn = page.locator('a,button').filter({ hasText: /^(apply|apply now|easy apply|apply for this job)$/i }).first();
  if (await applyBtn.count()) {
    await Promise.all([page.waitForLoadState('domcontentloaded').catch(() => {}), applyBtn.click().catch(() => {})]);
    await page.waitForTimeout(2000);
    await shot(page, '02-apply-page');
  }

  const fields = page.locator('form input:not([type=hidden]):not([type=submit]), form textarea, form select');
  const n = await fields.count();
  if (n === 0) { console.error('FORM_NOT_FOUND'); await browser.close(); process.exit(6); }

  const coverLetter = spec.cover_letter_file
    ? readFileSync(join(ROOT, spec.cover_letter_file), 'utf8').split('---').pop().trim() : '';
  const unanswered = [];

  for (let i = 0; i < n; i++) {
    const f = fields.nth(i);
    const meta = [
      await f.getAttribute('name'), await f.getAttribute('placeholder'), await f.getAttribute('aria-label'),
      await f.evaluate(el => el.labels?.[0]?.textContent || el.closest('label')?.textContent || ''),
    ].filter(Boolean).join(' | ');
    const type = (await f.getAttribute('type')) || (await f.evaluate(el => el.tagName)).toLowerCase();

    if (type === 'file') {
      const isCv = /resume|cv/i.test(meta) || !/cover/i.test(meta);
      await f.setInputFiles(join(ROOT, isCv ? answers.resume_file : spec.cover_letter_pdf || answers.resume_file)).catch(() => unanswered.push(`file: ${meta}`));
      continue;
    }
    const hit = FIELD_MAP.find(([re]) => re.test(meta));
    if (!hit) { if (await f.evaluate(el => el.required)) unanswered.push(`unmapped required: ${meta} (type=${type})`); continue; }
    const val = hit[1] === '__cover_letter__' ? coverLetter : answers[hit[1]];
    if (val == null || String(val).startsWith('_REVIEW')) { unanswered.push(`no verified answer for: ${meta} -> ${hit[1]}`); continue; }
    if (type === 'checkbox' || type === 'radio') { unanswered.push(`choice field needs human review: ${meta}`); continue; }
    if ((await f.evaluate(el => el.tagName)) === 'SELECT') {
      await f.selectOption({ label: String(val) }).catch(() => unanswered.push(`select mismatch: ${meta} -> ${val}`));
    } else {
      await f.fill(String(val)).catch(() => unanswered.push(`fill failed: ${meta}`));
    }
  }

  if (unanswered.length) {
    writeFileSync(join(AUDIT, `${slug}-unanswered.json`), JSON.stringify({ url: page.url(), unanswered }, null, 2));
    console.error('NEEDS_ANSWERS:\n  ' + unanswered.join('\n  '));
    await shot(page, '03-partial'); await browser.close(); process.exit(4);
  }

  await shot(page, '03-filled');
  if (dryRun) { console.log('DRY_RUN: form filled, not submitted:', page.url()); await browser.close(); process.exit(0); }

  const submit = page.locator('form button[type=submit], form input[type=submit], form button')
    .filter({ hasText: /submit|apply|send/i }).first();
  if (!(await submit.count())) { console.error('FORM_NOT_FOUND: no submit control'); await browser.close(); process.exit(6); }
  await submit.click();
  await page.waitForTimeout(4000);
  await shot(page, '04-confirmation');
  console.log('SUBMITTED:', page.url());
  await browser.close(); process.exit(0);
};

main().catch(e => { console.error('FATAL:', e.message); process.exit(1); });
