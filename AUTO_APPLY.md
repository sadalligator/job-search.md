# Auto-Apply Pipeline — instructions for the scheduled job-search agent

This repo now contains an application-submission engine. Every scheduled run (Mon/Wed/Fri 09:00
Dubai) must follow this pipeline. It exists because the Indeed MCP connector is search-only by
design — Indeed does not expose an apply tool — so submission happens through employer
application forms instead, or falls back to prepared-manual lanes.

## Current blockers and who can fix them

| # | Blocker | Status | Fix (owner: Tanya) |
|---|---------|--------|--------------------|
| 1 | Environment network policy blocks ALL job-site domains (proxy 403) | ACTIVE | claude.ai/code → this environment's settings → Network access → allow all domains, or add: `indeed.com`, `*.indeed.com`, `alcazarenergy.com`, `careers.marriott.com`, `rouse.com`, plus common ATS hosts (`*.smartrecruiters.com`, `*.workday.com`, `*.greenhouse.io`, `*.lever.co`, `boards.eu.greenhouse.io`) |
| 2 | Gmail connector authenticated but disabled in chat | ACTIVE | Chat connector settings → toggle Gmail ON (enables ready-to-send application drafts in your Gmail) |
| 3 | Indeed "Easily Apply" requires a logged-in human session | PERMANENT | Not automated from the cloud — Indeed's ToS prohibits bot submission on user accounts and it risks account suspension. Use the local lane below. |
| 4 | `tools/candidate_answers.json` has null fields (notice period, expected salary, start date) | ACTIVE | Fill the nulls; the engine refuses to guess them |

## Pipeline for every scheduled run

1. **Retry queue first.** Before new searches, take every `MANUAL_ACTION_REQUIRED` entry in
   `application_history.json` that has a spec file in `jobs/` and attempt it via the engine.
2. **Network preflight.** `curl -sS -o /dev/null -w "%{http_code}" https://www.indeed.com/` —
   on proxy 403, skip all engine attempts this run (statuses stay MANUAL_ACTION_REQUIRED; do
   not churn retries) and note blocker #1 in the report/notification.
3. **Resolve the real form.** Prefer the employer's own ATS posting (spec `alternate_urls`,
   or WebSearch "<company> <role> careers") over the Indeed link — employer forms are not
   login-walled; Indeed links usually are.
4. **Run the engine:**
   `node tools/auto_apply.mjs jobs/<spec>.json` (add `--dry-run` on first attempt of a new ATS
   domain, inspect `audit/` screenshots, then run live).
5. **Map exit codes to history statuses:**
   - `0` → `APPLIED` (attach audit screenshot paths in notes)
   - `3` → keep `MANUAL_ACTION_REQUIRED`, blocker "network policy"
   - `4` → `MANUAL_ACTION_REQUIRED`, copy the unanswered-fields list from `audit/*-unanswered.json`
     into notes so Tanya can add answers to `candidate_answers.json`
   - `5` → `MANUAL_ACTION_REQUIRED`, blocker "login/CAPTCHA — local browser lane"
   - `6` → investigate once, then manual
6. **Gmail lane (if the Gmail connector is available in the session).** For every role still
   manual, `create_draft` in Tanya's Gmail: to her own address, subject
   `APPLY TODAY: <Company> — <Role>`, body = apply link + tailored cover letter text. One tap
   from her phone replaces digging through the repo.
7. **Never**: invent answers, create accounts, enter credentials, or attempt CAPTCHA bypass.
   An application sent with wrong facts is worse than no application.

## Local lane for Indeed-walled roles (Tanya, ~2 min/role)

For roles only reachable through Indeed's own apply flow: open Claude Code on your laptop
(or Claude desktop with the Chrome extension), run it in this repo, and say
"apply to the roles in jobs/ using my logged-in browser". Claude drives your own authenticated
browser session — your account, your supervision, no ToS problem — and updates
`application_history.json` when done.

## Files

- `tools/auto_apply.mjs` — Playwright form-filler/submitter (exit codes above; screenshots to `audit/`)
- `tools/candidate_answers.json` — the ONLY source of screener answers; nulls are never guessed
- `jobs/*.json` — per-role specs (URL, cover letter, overrides) = the retry queue
- `audit/` — screenshots + unanswered-field dumps for every attempt (gitignored candidates; commit if useful)
