"""ตรวจ RUNBOOK.md แบบ objective แล้วพิมพ์ JSON ผลแต่ละข้อ"""
import json
import re
import sys
from pathlib import Path

repo = Path(sys.argv[1])
doc_path = repo / "RUNBOOK.md"
results = []


def check(text, passed, evidence):
    results.append({"text": text, "passed": bool(passed), "evidence": evidence})


if not doc_path.exists():
    check("RUNBOOK.md exists at the repo root", False, "file missing")
    print(json.dumps(results, ensure_ascii=False))
    sys.exit(0)

doc = doc_path.read_text(encoding="utf-8")
check("RUNBOOK.md exists at the repo root", True, f"{len(doc)} chars")

# 1. headings ตามลำดับ
want = ["## ภาพรวม", "## ตารางเวลา", "## คำสั่งที่ใช้บ่อย", "## การ Restore", "## Exit codes", "## การแก้ปัญหา"]
h2 = [l.strip() for l in doc.splitlines() if l.startswith("## ")]
check("The six R2 headings appear exactly and in order", h2 == want, f"found {h2}")

# 2. flags: ครบและไม่มีของปลอม
real = {"--config", "--verbose", "--target", "--dry-run", "--compress-level", "--snapshot", "--to", "--force", "--limit", "--json", "--help"}
mentioned = set(re.findall(r"(?<![\w-])--[a-z][a-z-]*", doc))
missing = sorted(real - {"--help"} - mentioned)
invented = sorted(mentioned - real)
check("Every CLI flag is documented", not missing, f"missing {missing}")
check("No invented flags appear", not invented, f"invented {invented}")
check("Subcommands run, restore, list, verify are all shown", all(re.search(rf"python -m backup[^\n`]*\b{c}\b", doc) for c in ["run", "restore", "list", "verify"]), "searched python -m backup <cmd>")

# 3. exit code table
section = doc.split("## Exit codes", 1)[-1].split("\n## ", 1)[0] if "## Exit codes" in doc else ""
table_rows = [l for l in section.splitlines() if l.strip().startswith("|")]
codes_in_table = {int(m) for l in table_rows for m in re.findall(r"^\|\s*`?(\d+)`?\s*\|", l.strip())}
need = {0, 2, 3, 4, 5, 6, 7, 8}
check("Exit code table lists 0, 2, 3, 4, 5, 6, 7", {0, 2, 3, 4, 5, 6, 7} <= codes_in_table, f"table codes {sorted(codes_in_table)}")
check("Exit code table includes 8 (disk space, only returned from restore.py)", 8 in codes_in_table, f"table codes {sorted(codes_in_table)}")
check("Exit code table rows have at least 3 columns (code, meaning, action)", table_rows and all(l.strip().strip("|").count("|") >= 2 for l in table_rows), f"{len(table_rows)} rows")

# 4. schedule, retention, bucket
check("Schedule is stated as 09:17 Bangkok time", re.search(r"0?9[:.]17", doc), "looked for 09:17")
check("Schedule is not stated as 02:17 Bangkok time", not re.search(r"0?2[:.]17[^\n]{0,30}(ไทย|Bangkok|กรุงเทพ|ICT|UTC\+7)", doc), "looked for 02:17 labelled Bangkok")
check("Retention of 14 days is stated", re.search(r"14\s*(วัน|days?)", doc), "looked for 14 วัน/days")
check("Bucket smc-prod-backups is named", "smc-prod-backups" in doc, "looked for bucket name")

# 5. restore dry-run ก่อน restore จริง
rs = doc.split("## การ Restore", 1)[-1].split("\n## ", 1)[0] if "## การ Restore" in doc else ""
cmds = [l for l in rs.splitlines() if "python -m backup" in l and " restore" in l]
first_dry = next((i for i, l in enumerate(cmds) if "--dry-run" in l), None)
first_real = next((i for i, l in enumerate(cmds) if "--dry-run" not in l), None)
check("Restore section runs --dry-run before the real restore", first_dry is not None and first_real is not None and first_dry < first_real, f"restore commands {cmds}")

# 6. code blocks, ภาษา, ความยาว
blocks = re.findall(r"```(\w*)\n(.*?)```", doc, re.S)
cmd_blocks = [b for b in blocks if "python -m backup" in b[1]]
check("Every code block with commands is fenced as bash", cmd_blocks and all(lang == "bash" for lang, _ in cmd_blocks), f"langs {[l for l, _ in cmd_blocks]}")
prose = re.sub(r"```.*?```", "", doc, flags=re.S)
prose = re.sub(r"`[^`]*`", "", prose)
thai = len(re.findall(r"[฀-๿]", prose))
latin = len(re.findall(r"[A-Za-z]", prose))
check("Prose is mainly Thai (Thai letters outnumber Latin letters outside code)", thai > latin, f"thai={thai} latin={latin}")
check("Under 6000 characters", len(doc) < 6000, f"{len(doc)} chars")

print(json.dumps(results, ensure_ascii=False))
