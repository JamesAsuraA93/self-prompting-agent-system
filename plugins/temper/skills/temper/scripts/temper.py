#!/usr/bin/env python3
"""temper bookkeeping: สร้าง run, บันทึกผล judge, และตัดสินว่าจะวนต่อหรือหยุด

ใช้คู่กับ SKILL.md ของ temper
ทุกคำสั่งพิมพ์บรรทัด KEY=VALUE ไว้ให้ agent อ่านต่อได้ตรง ๆ
"""

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = ".temper"
DEFAULT_MAX_ITERATIONS = 3
LEARNINGS_HEADER = "# Learnings\n\nบทเรียนที่ใช้ได้กับงานอื่นใน project นี้ ใส่ run id ที่สอนบทเรียนนั้นไว้ด้วย\n"


# 1. ตัวช่วยหา path และอ่าน/เขียน state
def state_dir(root: Path) -> Path:
    return root / STATE_DIR


def load_config(root: Path) -> dict:
    path = state_dir(root) / "config.json"
    if not path.exists():
        fail(f"ยังไม่ได้ init ที่ {root} ให้รัน `temper.py init` ก่อน")
    return json.loads(path.read_text(encoding="utf-8"))


def load_log(root: Path) -> list[dict]:
    path = state_dir(root) / "log.jsonl"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def write_log(root: Path, entries: list[dict]) -> None:
    path = state_dir(root) / "log.jsonl"
    body = "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries)
    path.write_text(body, encoding="utf-8")


def fail(message: str) -> None:
    print(f"❌ {message}")
    sys.exit(1)


# 2. init: สร้างโฟลเดอร์ state (รันซ้ำได้ ไม่ทับของเดิม)
def cmd_init(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    sdir = state_dir(root)
    (sdir / "runs").mkdir(parents=True, exist_ok=True)

    config_path = sdir / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    if args.max is not None:
        if args.max < 1:
            fail("--max ต้องมากกว่า 0")
        config["max_iterations"] = args.max
    config.setdefault("max_iterations", DEFAULT_MAX_ITERATIONS)
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    learnings = sdir / "learnings.md"
    if not learnings.exists():
        learnings.write_text(LEARNINGS_HEADER, encoding="utf-8")

    print(f"✅ พร้อมใช้งานที่ {sdir} (max_iterations = {config['max_iterations']})")
    print(f"STATE_DIR={sdir}")
    print(f"MAX_ITERATIONS={config['max_iterations']}")


# 3. new-run: สร้างโฟลเดอร์ run ใหม่ เลขรันต่อจากของเดิม
def cmd_new_run(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    load_config(root)
    runs = state_dir(root) / "runs"
    numbers = [int(p.name[:3]) for p in runs.iterdir() if p.is_dir() and p.name[:3].isdigit()]
    next_number = max(numbers, default=0) + 1
    run_id = f"{next_number:03d}"
    if args.label:
        slug = "".join(c if c.isalnum() else "-" for c in args.label.lower()).strip("-")
        run_id = f"{run_id}-{slug}"
    run_dir = runs / run_id
    run_dir.mkdir()
    print(f"✅ สร้าง run ใหม่แล้ว: {run_dir}")
    print(f"RUN_ID={run_id}")
    print(f"RUN_DIR={run_dir}")


# 4. record: บันทึกผล judge แล้วตัดสินใจ
def score(e: dict) -> tuple[int, int]:
    return (e["passed"], e.get("advisory_passed", 0))


def decide(history: list[dict], current: dict, max_iterations: int) -> tuple[str, int, list[str]]:
    """คืนค่า (decision, best_version, regressed_ids)

    เทียบเวอร์ชันด้วย (hard ที่ผ่าน, advisory ที่ผ่าน) hard สำคัญกว่าเสมอ
    advisory ช่วยตัดสินเฉพาะตอน hard เท่ากัน
    """
    previous = [e for e in history if e["version"] < current["version"]]
    regressed: list[str] = []
    if previous:
        last = max(previous, key=lambda e: e["version"])
        now_failed = set(current["failed"]) | set(current.get("advisory_failed", []))
        was_failed = set(last["failed"]) | set(last.get("advisory_failed", []))
        regressed = sorted(now_failed - was_failed)

    everything = previous + [current]
    # เวอร์ชันที่ดีที่สุด = คะแนนสูงสุด ถ้าเท่ากันเอาเวอร์ชันแรกสุด (แก้น้อยกว่า)
    best = max(everything, key=lambda e: (score(e), -e["version"]))
    hard_pass = current["passed"] == current["total"]
    advisory_pass = not current.get("advisory_failed")

    if hard_pass and advisory_pass:
        return "stop_pass", current["version"], regressed
    if previous and score(current) <= max(score(e) for e in previous):
        return "stop_plateau", best["version"], regressed
    if current["version"] >= max_iterations:
        return "stop_max", best["version"], regressed
    if hard_pass:
        return "pass_with_advisory", current["version"], regressed
    return "continue", best["version"], regressed


def cmd_record(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    config = load_config(root)
    run_dir = state_dir(root) / "runs" / args.run_id
    if not run_dir.is_dir():
        fail(f"ไม่เจอ run {args.run_id} ใน {run_dir.parent}")
    if args.version < 1:
        fail("--version ต้องเริ่มที่ 1")
    if args.total < 1:
        fail("--total ต้องมีอย่างน้อย 1 criterion")

    failed = sorted({x.strip() for x in args.failed.split(",") if x.strip()})
    if len(failed) > args.total:
        fail(f"จำนวน failed ({len(failed)}) มากกว่า total ({args.total})")
    advisory_failed = sorted({x.strip() for x in args.advisory_failed.split(",") if x.strip()})
    if len(advisory_failed) > args.advisory_total:
        fail(f"จำนวน advisory-failed ({len(advisory_failed)}) มากกว่า advisory-total ({args.advisory_total})")

    current = {
        "run": args.run_id,
        "version": args.version,
        "total": args.total,
        "passed": args.total - len(failed),
        "failed": failed,
        "advisory_total": args.advisory_total,
        "advisory_passed": args.advisory_total - len(advisory_failed),
        "advisory_failed": advisory_failed,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    log = load_log(root)
    replaced = any(e["run"] == args.run_id and e["version"] == args.version for e in log)
    log = [e for e in log if not (e["run"] == args.run_id and e["version"] == args.version)]
    history = [e for e in log if e["run"] == args.run_id]
    if any(e["total"] != args.total for e in history):
        print("⚠️ total ไม่เท่ากับเวอร์ชันก่อน (reqs.md เปลี่ยนกลางทาง?) ผลเทียบกันอาจไม่ตรง")
    decision, best_version, regressed = decide(history, current, config["max_iterations"])
    current["decision"] = decision
    current["best_version"] = best_version
    write_log(root, log + [current])

    if replaced:
        print(f"ℹ️ เขียนทับผลเดิมของ v{args.version}")
    print(f"📊 run {args.run_id} v{args.version}: ผ่าน {current['passed']}/{current['total']}")
    if failed:
        print(f"   ยังไม่ผ่าน: {', '.join(failed)}")
    if args.advisory_total:
        print(f"   advisory ผ่าน {current['advisory_passed']}/{args.advisory_total}" + (f" (ยังไม่ผ่าน: {', '.join(advisory_failed)})" if advisory_failed else ""))
    if regressed:
        print(f"⚠️ เคยผ่านแต่ตอนนี้พัง: {', '.join(regressed)}")

    messages = {
        "stop_pass": "✅ ผ่านครบทุกข้อ หยุดได้",
        "stop_plateau": f"🛑 คะแนนไม่ดีขึ้นกว่าเดิม หยุด แล้วกลับไปใช้ v{best_version} (น่าจะไม่ใช่ปัญหาที่ prompt แล้ว)",
        "stop_max": f"🛑 ครบ {config['max_iterations']} รอบแล้ว หยุด เวอร์ชันที่ดีที่สุดคือ v{best_version}",
        "pass_with_advisory": f"🟡 hard criteria ผ่านครบ แต่ข้อ [judgment] ยังไม่ผ่าน ถามผู้ใช้ก่อนว่าจะทำ v{args.version + 1} ต่อไหม (หรือทำต่อเลยถ้าผู้ใช้สั่งไว้แล้ว)",
        "continue": (
            f"🔁 ดีขึ้นแต่ยังไม่ครบ วนต่อไป v{args.version + 1}"
            if history
            else f"🔁 ยังไม่ครบ วนต่อไป v{args.version + 1}"
        ),
    }
    print(messages[decision])
    print(f"DECISION={decision}")
    print(f"BEST_VERSION={best_version}")
    print(f"REGRESSED={','.join(regressed)}")


# 5. dream: เตรียมข้อมูลให้ dream pass, snapshot learnings, และปิด dream
def learnings_sha(root: Path) -> str:
    path = state_dir(root) / "learnings.md"
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""


def last_dream(root: Path) -> dict | None:
    dreams = state_dir(root) / "dreams"
    done = sorted(dreams.glob("*/done.json")) if dreams.exists() else []
    return json.loads(done[-1].read_text(encoding="utf-8")) if done else None


def cmd_dream_prep(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    load_config(root)
    log = load_log(root)
    if not log:
        fail("ยังไม่มี run ที่บันทึกผลไว้ ยังไม่มีอะไรให้ dream")

    sdir = state_dir(root)
    dreams = sdir / "dreams"
    dreams.mkdir(exist_ok=True)
    open_dreams = [d.name for d in dreams.iterdir() if d.is_dir() and not (d / "done.json").exists()]
    if open_dreams:
        print(f"⚠️ มี dream ที่ยังไม่ปิด: {', '.join(sorted(open_dreams))} (ถ้าทิ้งแล้วให้ลบโฟลเดอร์นั้น หรือรัน dream-done)")

    previous = last_dream(root)
    reviewed_before = set(previous["runs"]) if previous else set()

    runs = []
    for run_id in sorted({e["run"] for e in log}):
        entries = sorted((e for e in log if e["run"] == run_id), key=lambda e: e["version"])
        run_dir = sdir / "runs" / run_id
        files = sorted(p.name for p in run_dir.iterdir()) if run_dir.is_dir() else []
        runs.append({
            "run": run_id,
            "dir": str(run_dir),
            "new_since_last_dream": run_id not in reviewed_before,
            "versions": [
                {k: e.get(k) for k in ("version", "passed", "total", "failed", "decision")} for e in entries
            ],
            "final_decision": entries[-1].get("decision", "unknown"),
            "files": files,
        })

    # นับ criterion id ที่พังในหลาย run (นับเป็น run ไม่ใช่ version)
    failing_runs: dict[str, set[str]] = {}
    for r in runs:
        for v in r["versions"]:
            for cid in v["failed"] or []:
                failing_runs.setdefault(cid, set()).add(r["run"])
    repeated = {cid: sorted(rs) for cid, rs in failing_runs.items() if len(rs) >= 2}

    numbers = [int(d.name[:3]) for d in dreams.iterdir() if d.is_dir() and d.name[:3].isdigit()]
    dream_id = f"{max(numbers, default=0) + 1:03d}"
    dream_dir = dreams / dream_id
    dream_dir.mkdir()
    manifest = {
        "dream": dream_id,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "learnings_sha256": learnings_sha(root),
        "learnings_path": str(sdir / "learnings.md"),
        "log_path": str(sdir / "log.jsonl"),
        "runs": runs,
        "summary": {
            "runs": len(runs),
            "new_since_last_dream": sum(r["new_since_last_dream"] for r in runs),
            "needed_more_than_one_version": sum(len(r["versions"]) > 1 for r in runs),
            "final_decisions": {d: sum(r["final_decision"] == d for r in runs) for d in sorted({r["final_decision"] for r in runs})},
            "criteria_failing_in_2_plus_runs": repeated,
        },
    }
    (dream_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    s = manifest["summary"]
    print(f"✅ เตรียม dream {dream_id} แล้ว: {s['runs']} run (ใหม่ {s['new_since_last_dream']}), ต้องแก้มากกว่า 1 รอบ {s['needed_more_than_one_version']} run")
    if repeated:
        print(f"   criterion ที่พังซ้ำหลาย run: {', '.join(f'{k} ({len(v)})' for k, v in repeated.items())} (id อาจหมายถึงคนละข้อถ้า reqs.md เปลี่ยน)")
    print(f"DREAM_ID={dream_id}")
    print(f"DREAM_DIR={dream_dir}")
    print(f"LEARNINGS_SHA={manifest['learnings_sha256']}")
    print(f"RUNS={','.join(r['run'] for r in runs)}")


def cmd_snapshot(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    load_config(root)
    current = learnings_sha(root)
    if args.expect is not None and current != args.expect:
        fail("learnings.md ถูกแก้ไปแล้วหลังเริ่ม dream (มี run อื่นหรือคนแก้ระหว่างนั้น) ให้รัน dream ใหม่ อย่าเขียนทับ")
    history = state_dir(root) / "learnings.history"
    history.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = history / f"{stamp}.md"
    n = 2
    while target.exists():
        target = history / f"{stamp}-{n}.md"
        n += 1
    shutil.copy2(state_dir(root) / "learnings.md", target)
    print(f"✅ เก็บสำเนา learnings.md ไว้ที่ {target} แก้ได้เลย")
    print(f"SNAPSHOT={target}")


def cmd_dream_done(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    load_config(root)
    dream_dir = state_dir(root) / "dreams" / args.dream_id
    manifest_path = dream_dir / "manifest.json"
    if not manifest_path.exists():
        fail(f"ไม่เจอ dream {args.dream_id}")
    if not (dream_dir / "applied.md").exists():
        fail("ยังไม่มี applied.md ให้บันทึกก่อนว่ารับหรือไม่รับข้อไหน (ถึงไม่รับเลยก็เขียนไว้)")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    done = {
        "dream": args.dream_id,
        "done_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "runs": [r["run"] for r in manifest["runs"]],
        "learnings_sha256_after": learnings_sha(root),
    }
    (dream_dir / "done.json").write_text(json.dumps(done, indent=2) + "\n", encoding="utf-8")
    print(f"✅ ปิด dream {args.dream_id} แล้ว ({len(done['runs'])} run)")


# 6. status: สรุปทุก run ที่เคยบันทึกไว้
def cmd_status(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    config = load_config(root)
    log = load_log(root)
    if not log:
        print("ℹ️ ยังไม่มีผลที่บันทึกไว้")
        return
    print(f"📋 max_iterations = {config['max_iterations']}")
    for run_id in sorted({e["run"] for e in log}):
        entries = sorted((e for e in log if e["run"] == run_id), key=lambda e: e["version"])
        trail = "  ".join(f"v{e['version']} {e['passed']}/{e['total']}" + (f" (+{e['advisory_passed']}/{e['advisory_total']} adv)" if e.get("advisory_total") else "") for e in entries)
        print(f"   {run_id}: {trail}")

    previous = last_dream(root)
    reviewed = set(previous["runs"]) if previous else set()
    pending = len({e["run"] for e in log} - reviewed)
    where = f"dream ล่าสุด {previous['dream']}" if previous else "ยังไม่เคย dream"
    print(f"🌙 {where}, มี run ใหม่ {pending} run ตั้งแต่นั้น")
    if pending >= 5:
        print("   ถึงเวลา dream แล้ว (รัน dream-prep)")
    print(f"RUNS_SINCE_DREAM={pending}")


# 7. ตั้งค่า argument parser
def main() -> None:
    parser = argparse.ArgumentParser(description="temper bookkeeping")
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="create .temper state")
    p_init.add_argument("--max", type=int, help="max iterations per run")
    p_init.set_defaults(func=cmd_init)

    p_new = sub.add_parser("new-run", help="create a new run directory")
    p_new.add_argument("--label", help="short label added to the run id")
    p_new.set_defaults(func=cmd_new_run)

    p_rec = sub.add_parser("record", help="record a judge result and decide")
    p_rec.add_argument("run_id")
    p_rec.add_argument("--version", type=int, required=True)
    p_rec.add_argument("--total", type=int, required=True, help="hard criteria count")
    p_rec.add_argument("--failed", required=True, help='comma separated ids, "" when all passed')
    p_rec.add_argument("--advisory-total", type=int, default=0, help="[judgment] criteria count")
    p_rec.add_argument("--advisory-failed", default="", help="failed [judgment] ids")
    p_rec.set_defaults(func=cmd_record)

    p_dream = sub.add_parser("dream-prep", help="collect finished runs for a dream pass")
    p_dream.set_defaults(func=cmd_dream_prep)

    p_snap = sub.add_parser("snapshot", help="copy learnings.md to history before editing it")
    p_snap.add_argument("--expect", help="sha256 from dream-prep; refuse if learnings.md changed since")
    p_snap.set_defaults(func=cmd_snapshot)

    p_done = sub.add_parser("dream-done", help="close a dream after applying the accepted changes")
    p_done.add_argument("dream_id")
    p_done.set_defaults(func=cmd_dream_done)

    p_status = sub.add_parser("status", help="show results so far")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
