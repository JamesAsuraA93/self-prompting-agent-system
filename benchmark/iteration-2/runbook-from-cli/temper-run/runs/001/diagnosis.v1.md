# Diagnosis v1

Hard criteria: 5 of 6 passed. AC3 failed, and the judge's must-have probing flagged R3 and R4.
The script returned continue, but both causes are requirements gaps, so the loop stops here and asks the owner (SKILL.md Step 5).

## AC3 / R4: requirements gap
Evidence: judge.v1.md. `python -m backup restore --snapshot abc --to /nonexistent/dir --dry-run` crashes with an uncaught FileNotFoundError and exits 1, and the exit code table has no row for 1. The runbook already tells on-call to create the target directory first.
Question for the owner: does a crash exit (an uncaught exception) count as "a code the CLI can return", or only the codes the code returns on purpose?

## R3: requirements gap
Evidence: judge.v1.md. argparse accepts `-h/--help` automatically, and the runbook does not mention it. AC2 only checks flags defined in `backup/cli.py`, which `--help` is not.
Question for the owner: should "every flag the CLI accepts" include argparse's built-in help flag?
