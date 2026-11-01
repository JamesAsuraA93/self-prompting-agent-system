# On-call runbook for the backup CLI

## Goal
Write `RUNBOOK.md` at the repo root so whoever is on call can operate and troubleshoot the nightly backup without reading the code.

## Why
The person who wrote this tool left, and the last restore took two hours because nobody knew which flags existed or what exit 5 meant.
On-call engineers on this team read Thai first, so the runbook should read naturally to them.

## Users and context
Thai-speaking on-call engineers, at night, under pressure.
The CLI lives in `backup/`, the schedule in `deploy/crontab`.
The servers run on UTC, the team works in Bangkok time (UTC+7).

## Must have
- R1: Prose is in Thai. Commands, flags, file paths, and technical terms (backup, restore, snapshot, bucket, exit code, cron) stay in English.
- R2: These second-level headings, in this order: `## ภาพรวม`, `## ตารางเวลา`, `## คำสั่งที่ใช้บ่อย`, `## การ Restore`, `## Exit codes`, `## การแก้ปัญหา`.
- R3: Every flag the CLI accepts is documented, and no flag that does not exist appears anywhere in the runbook.
- R4: Every exit code the CLI can return is in a Markdown table with its meaning and what on-call should do.
- R5: The schedule is stated in Bangkok time.
- R6: The retention period and the bucket name are stated, taken from the code.
- R7: The restore procedure runs a dry run before the real restore.
- R8: Commands are in fenced `bash` code blocks and use the real invocation `python -m backup`.
- R9: Under 6000 characters in total, so it fits on a couple of screens.

## Constraints
Only add `RUNBOOK.md`; do not change the code.

## Out of scope
Architecture explanations, setting up the cron job, and anything about the internals of the storage provider.

## Acceptance criteria
- AC1: The six headings from R2 exist in that order.
- AC2: Every flag defined in `backup/cli.py` appears in the runbook, and every `--flag` in the runbook exists in `backup/cli.py`.
- AC3: The exit code table covers every code the CLI can return, each with a meaning and an action.
- AC4: The schedule is given as a Bangkok time that matches `deploy/crontab`.
- AC5: Retention and bucket name match `backup/config.py`.
- AC6: In the restore section, a `--dry-run` restore command appears before the restore command without it.
- AC7: [judgment] An on-call engineer reading only the runbook could restore a snapshot and react to every exit code.
