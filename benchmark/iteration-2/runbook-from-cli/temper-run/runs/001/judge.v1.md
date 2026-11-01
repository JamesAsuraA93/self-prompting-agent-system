# Verdict

Hard criteria: 5 of 6 passed
Failed or unclear: AC3
Must-have requirements not met: R3, R4

All checks below ran against a copy of `backup/` in a scratch directory, so the repo was not touched (no `__pycache__` was created in it).

## AC1: The six headings from R2 exist in that order.
Verdict: PASS
Evidence: `re.findall(r'^## .*', RUNBOOK.md)` returned
`['## ภาพรวม', '## ตารางเวลา', '## คำสั่งที่ใช้บ่อย', '## การ Restore', '## Exit codes', '## การแก้ปัญหา']`
That is exactly the R2 list, in order, with no extra H2s.

## AC2: Every flag defined in `backup/cli.py` appears in the runbook, and every `--flag` in the runbook exists in `backup/cli.py`.
Verdict: PASS
Evidence: regex extraction from both files gave the same set:
- runbook: `['--compress-level', '--config', '--dry-run', '--force', '--json', '--limit', '--snapshot', '--target', '--to', '--verbose']`
- cli.py: `['--compress-level', '--config', '--dry-run', '--force', '--json', '--limit', '--snapshot', '--target', '--to', '--verbose']`
I also ran every command the runbook gives (`--config ... --verbose list`, `run --target db --dry-run`, `run --target all --compress-level 6`, `list --limit 5`, `list --json`, `verify --snapshot abc`, `restore ... --dry-run`, `restore ...`, `restore ... --force`, `--verbose verify --snapshot abc`). Each one exited 0, so every documented invocation parses. The runbook says global flags must come before the subcommand, and that is correct: `list --verbose` gives `exit=2 ... error: unrecognized arguments: --verbose`.

## AC3: The exit code table covers every code the CLI can return, each with a meaning and an action.
Verdict: FAIL
Evidence: the table has rows for 0, 2, 3, 4, 5, 6, 7 and 8. Each row has a meaning and an action. 8 is the code returned literally in `restore.py:12`, and the table gets it right (`| 8 | ที่ว่างบน directory ปลายทางของ restore น้อยกว่า 5 GiB | แจ้ง infra ให้ขยาย volume ...`). I confirmed it by forcing low free space: `dry-run exit 8`. The CLI can also return 1, and the table does not list it:
`python -m backup restore --snapshot abc --to /nonexistent/dir --dry-run` gave `exit=1`, `FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/dir'` (raised by `shutil.disk_usage(args.to)` in `restore.py:9`).
Note: this is very close. Every code the code defines or returns explicitly is covered and correct. Step 2 of the restore procedure also says the target must exist (`ต้องมีอยู่จริง`, `mkdir -p`), which prevents the crash on the happy path. But on-call who hit exit 1 with a traceback (for example from a typo in `--to`) would find nothing in the table. One row for exit 1 (unhandled error / traceback, check that `--to` exists, then read the traceback and escalate) would fix it. Ambiguity: the requirements do not say whether exits from an uncaught Python exception count as "codes the CLI can return". If they should not count, the requirements should say so. I graded it strictly and literally.

## AC4: The schedule is given as a Bangkok time that matches `deploy/crontab`.
Verdict: PASS
Evidence: crontab: `17 2 * * * backup cd /opt/backup && python -m backup run --target all ...`, with the comment `# server clock is UTC`. Runbook: `cron รันทุกวันเวลา **09:17 น. เวลากรุงเทพฯ** (นาฬิกาเซิร์ฟเวอร์เป็น UTC: `17 2 * * *` คือ 02:17 UTC)`. 02:17 UTC + 7 = 09:17 Bangkok, which is correct.

## AC5: Retention and bucket name match `backup/config.py`.
Verdict: PASS
Evidence: config.py has `BUCKET = os.environ.get("BACKUP_BUCKET", "smc-prod-backups")` and `RETENTION_DAYS = 14`. Runbook: `- Bucket: `smc-prod-backups` (เปลี่ยนได้ด้วย env var `BACKUP_BUCKET`)` and `- Retention: เก็บ snapshot ไว้ 14 วัน (`RETENTION_DAYS = 14`)`.

## AC6: In the restore section, a `--dry-run` restore command appears before the restore command without it.
Verdict: PASS
Evidence: in `## การ Restore`, step 4 (line 102) is `python -m backup restore --snapshot <id> --to /restore/target --dry-run`. Step 5 (line 108) is `python -m backup restore --snapshot <id> --to /restore/target`. No restore command without `--dry-run` comes before line 102.

## Advisory
AC7 [judgment]: an on-call engineer reading only the runbook could restore a snapshot and react to every exit code. Verdict: PASS (advisory), with one gap. The restore procedure is complete and in a sensible order: list, prepare the target and check free space (which pre-empts exit 8), verify, dry run, real restore, optional `--force` with a confirmation step, then check `$?`. Every documented code has a concrete action, and the troubleshooting section adds commands for exits 7, 8 and 5. The runbook also notes that the disk check applies to the dry run too, which is correct per `restore.py`. The gap is exit 1 (see AC3): a traceback has no guidance. The stale-lock advice (`rm /var/run/backup.lock`) cannot be checked against the code, because no lock handling exists in this repo. It is reasonable advice, but it is not sourced from the code.

## Must-have requirements
- R1 (Thai prose, English terms): met. All explanatory prose is Thai. Commands, flags, paths and terms stay in English. Minor: the H1 `# RUNBOOK: Nightly backup CLI` and a few words (`escalate`, `machine-readable`, `Usage error`) are English, but these are borderline technical terms, not prose sentences.
- R2: met (AC1).
- R3: NOT MET (literal reading). argparse adds `-h/--help` automatically, and the CLI accepts it (`python -m backup --help` gives `exit=0`), but the runbook never mentions it. No nonexistent flag appears (AC2). Ambiguity: AC2 checks only flags "defined in `backup/cli.py`", so it passes. R3 says "every flag the CLI accepts", so it does not. The requirements should say whether the auto-generated `--help` counts.
- R4: NOT MET. Exit 1 is reachable and not in the table (AC3).
- R5: met (AC4).
- R6: met (AC5).
- R7: met (AC6). The `run` re-run in troubleshooting also does a dry run first.
- R8: met. All 18 fenced blocks are tagged `bash`, and every CLI invocation in them uses `python -m backup`. A scan for `python` + `backup` lines without `python -m backup` returned nothing.
- R9: met. `len(open('RUNBOOK.md', encoding='utf-8').read())` gives `4664` characters (7602 bytes in UTF-8). Even the byte count would be over 6000, so "characters" must be read as Unicode characters, which is the natural reading.

## Other observations
- Constraint "only add RUNBOOK.md": I could not diff this, because the repo is not a git repository. The code files look unmodified and consistent with each other, and no stray files exist besides `RUNBOOK.md`, `reqs.md`, `backup/` and `deploy/`.
- In this repo, exits 3, 4, 6 and 7 are defined in `exitcodes.py` but no code path returns them (the comment says "wired up in the real service"). Documenting them is correct for the real service.
