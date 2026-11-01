# Task
Write `RUNBOOK.md` at the repo root: an on-call runbook for the nightly backup CLI, so whoever is on call can run, restore, and troubleshoot it without reading the code.
Only add this file; do not change any code.

## Why this matters
The person who wrote the tool left.
The last restore took two hours because nobody knew which flags existed or what exit 5 meant.
The readers are Thai-speaking on-call engineers, at night, under pressure, so the runbook must read naturally in Thai, be short, and be exactly right about commands.

## Context
Read every file in `backup/` and `deploy/` before writing; the facts below are what they contain, and the runbook must match the code exactly.
- `backup/cli.py`, `build_parser()`: the invocation is `python -m backup`. Global flags `--config` (default from `config.DEFAULT_CONFIG_PATH`) and `--verbose`. Subcommands:
  - `run`: `--target {db,files,all}` (default all), `--dry-run`, `--compress-level` (zstd level 1-19, default 6)
  - `restore`: `--snapshot` (required, id from `list`), `--to` (required, target directory), `--dry-run`, `--force` (overwrite a non-empty target)
  - `list`: `--limit` (default 20), `--json`
  - `verify`: `--snapshot` (required)
- `backup/exitcodes.py`: 0 OK, 3 CONFIG_ERROR, 4 STORAGE_UNREACHABLE, 5 SNAPSHOT_NOT_FOUND, 6 CHECKSUM_MISMATCH, 7 LOCK_HELD. A comment notes that 2 is argparse's own usage error.
- `backup/restore.py` also returns 8 when the target has less than 5 GiB free; the comment says to ask infra to expand the volume. It is not in exitcodes.py, but the CLI can return it.
- `backup/config.py`: bucket `smc-prod-backups` (overridable with the `BACKUP_BUCKET` env var), `RETENTION_DAYS = 14`, lock file `/var/run/backup.lock`, default config `/etc/backup/config.toml`.
- `deploy/crontab`: `17 2 * * *` on a server clock that is UTC, running `python -m backup run --target all`, logging to `/var/log/backup.log`. The team works in Bangkok time (UTC+7), so convert.

## What to deliver
One file, `RUNBOOK.md`, at the repo root, under 6000 characters.

## Requirements
- R1: Prose is in Thai. Commands, flags, file paths, and technical terms (backup, restore, snapshot, bucket, exit code, cron) stay in English.
- R2: These second-level headings, in this order: `## ภาพรวม`, `## ตารางเวลา`, `## คำสั่งที่ใช้บ่อย`, `## การ Restore`, `## Exit codes`, `## การแก้ปัญหา`.
- R3: Every flag the CLI accepts is documented, and no flag that does not exist appears anywhere in the runbook.
- R4: Every exit code the CLI can return is in a Markdown table with its meaning and what on-call should do.
- R5: The schedule is stated in Bangkok time.
- R6: The retention period and the bucket name are stated, taken from the code.
- R7: The restore procedure runs a dry run before the real restore.
- R8: Commands are in fenced `bash` code blocks and use the real invocation `python -m backup`.
- R9: Under 6000 characters in total, so it fits on a couple of screens.


## Constraints and out of scope
Only add RUNBOOK.md.
No architecture explanations, cron setup instructions, or storage-provider internals.

## Acceptance criteria
- AC1: The six headings from R2 exist in that order.
- AC2: Every flag defined in `backup/cli.py` appears in the runbook, and every `--flag` in the runbook exists in `backup/cli.py`.
- AC3: The exit code table covers every code the CLI can return, each with a meaning and an action.
- AC4: The schedule is given as a Bangkok time that matches `deploy/crontab`.
- AC5: Retention and bucket name match `backup/config.py`.
- AC6: In the restore section, a `--dry-run` restore command appears before the restore command without it.
- AC7: [judgment] An on-call engineer reading only the runbook could restore a snapshot and react to every exit code.

## When something is unclear
Make the reasonable choice and keep going.
List each assumption in your final report.

## Before you finish
Count the characters of RUNBOOK.md, and grep it for every `--` token to confirm each one is real.
Check your work against every acceptance criterion; for each one, report PASS or FAIL and how you checked it.
