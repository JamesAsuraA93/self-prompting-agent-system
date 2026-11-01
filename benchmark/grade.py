"""ให้คะแนนผลลัพธ์ทุก run ด้วย hidden tests แล้วเขียน grading.json"""
import filecmp
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HIDDEN = ROOT / "hidden"
FIXTURES = ROOT.parent / "plugins/temper/skills/temper/evals"


# 1. ตัวช่วยเทียบไฟล์ที่ห้ามแก้
def unchanged(repo: Path, case: str, rel: str) -> bool:
    a, b = FIXTURES / case / "files" / rel, repo / rel
    if a.is_dir():
        cmp = filecmp.dircmp(a, b, ignore=["__pycache__"])
        def same(c):
            return not (c.left_only or c.diff_files) and all(same(s) for s in c.subdirs.values())
        return same(cmp)
    return b.exists() and filecmp.cmp(a, b, shallow=False)


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
    return p.returncode, (p.stdout + p.stderr)


# 2. แต่ละ case
def grade_csv(repo: Path):
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(repo, work, ignore=shutil.ignore_patterns(".temper", "__pycache__", ".pytest_cache"))
        shutil.copy(HIDDEN / "test_hidden_csv.py", work / "tests" / "test_hidden_csv.py")
        xml = Path(tmp) / "r.xml"
        run(["pytest", "-q", "tests/test_hidden_csv.py", f"--junitxml={xml}"], work)
        for tc in ET.parse(xml).getroot().iter("testcase"):
            failed = tc.find("failure") is not None or tc.find("error") is not None
            msg = ""
            if failed:
                node = tc.find("failure") if tc.find("failure") is not None else tc.find("error")
                msg = (node.get("message") or "")[:300]
            out.append({"text": f"hidden: {tc.get('name')}", "passed": not failed, "evidence": msg or "passed"})
        (work / "tests" / "test_hidden_csv.py").unlink()
        code, log = run(["pytest", "-q"], work)
        out.append({"text": "The repo's own test suite passes", "passed": code == 0, "evidence": log.strip().splitlines()[-1] if log.strip() else ""})
    out.append({"text": "shop/orders.py is unchanged", "passed": unchanged(repo, "csv-export-thai", "shop/orders.py"), "evidence": "byte compare with fixture"})
    return out


def grade_duration(repo: Path):
    out = []
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        shutil.copytree(repo, work, ignore=shutil.ignore_patterns(".temper", "node_modules"))
        shutil.copy(HIDDEN / "hidden_duration.test.js", work / "test" / "hidden_duration.test.js")
        _, log = run(["node", "--test", "--test-reporter=tap", "test/hidden_duration.test.js"], work)
        for m in re.finditer(r"^(not ok|ok) \d+ - (.+)$", log, re.M):
            out.append({"text": f"hidden: {m.group(2)}", "passed": m.group(1) == "ok", "evidence": "passed" if m.group(1) == "ok" else "failed (see tap output)"})
        if not out:
            out.append({"text": "hidden suite loads", "passed": False, "evidence": log[:300]})
        (work / "test" / "hidden_duration.test.js").unlink()
        code, log = run(["npm", "test", "--silent"], work)
        tail = [l for l in log.splitlines() if l.startswith("# pass") or l.startswith("# fail")]
        out.append({"text": "The repo's own test suite passes", "passed": code == 0, "evidence": " ".join(tail)})
    return out


def grade_runbook(repo: Path):
    _, log = run([sys.executable, str(HIDDEN / "check_runbook.py"), str(repo)], ROOT)
    out = json.loads(log)
    ok = unchanged(repo, "runbook-from-cli", "backup") and unchanged(repo, "runbook-from-cli", "deploy")
    out.append({"text": "Code in backup/ and deploy/ is unchanged", "passed": ok, "evidence": "dir compare with fixture"})
    return out


GRADERS = {"csv-export-thai": grade_csv, "parse-duration": grade_duration, "runbook-from-cli": grade_runbook}

# 3. วนทุก case/config แล้วเขียน grading.json
iteration = Path(sys.argv[1])
for case, fn in GRADERS.items():
    for cfg in ("with_skill", "without_skill"):
        run_dir = iteration / case / cfg
        repo = run_dir / "outputs" / "repo"
        if not repo.exists():
            continue
        exp = fn(repo)
        passed = sum(e["passed"] for e in exp)
        grading = {"expectations": exp, "summary": {"passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": round(passed / len(exp), 4)}}
        (run_dir / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2), encoding="utf-8")
        fails = [e["text"] for e in exp if not e["passed"]]
        print(f"{'✅' if not fails else '⚠️'} {case}/{cfg}: {passed}/{len(exp)}")
        for f in fails:
            print(f"     ❌ {f}")
