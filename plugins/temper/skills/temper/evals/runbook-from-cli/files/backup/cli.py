import argparse

from backup import config, exitcodes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m backup", description="Nightly backups to object storage")
    parser.add_argument("--config", default=config.DEFAULT_CONFIG_PATH, help="path to config.toml")
    parser.add_argument("--verbose", action="store_true", help="log every file")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="take a snapshot now")
    run.add_argument("--target", choices=["db", "files", "all"], default="all")
    run.add_argument("--dry-run", action="store_true", help="show what would be uploaded")
    run.add_argument("--compress-level", type=int, default=6, help="zstd level 1-19")

    restore = sub.add_parser("restore", help="restore a snapshot")
    restore.add_argument("--snapshot", required=True, help="snapshot id from `list`")
    restore.add_argument("--to", required=True, help="directory to restore into")
    restore.add_argument("--dry-run", action="store_true", help="list files without writing")
    restore.add_argument("--force", action="store_true", help="overwrite a non-empty target directory")

    ls = sub.add_parser("list", help="list snapshots")
    ls.add_argument("--limit", type=int, default=20)
    ls.add_argument("--json", action="store_true", help="machine-readable output")

    verify = sub.add_parser("verify", help="check a snapshot's checksums")
    verify.add_argument("--snapshot", required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "restore":
        from backup.restore import restore_snapshot

        return restore_snapshot(args)
    # the other commands are wired up in the real service
    return exitcodes.OK
