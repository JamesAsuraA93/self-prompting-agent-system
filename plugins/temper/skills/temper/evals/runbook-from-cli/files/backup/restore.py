import shutil

from backup import exitcodes

MIN_FREE_BYTES = 5 * 1024**3


def restore_snapshot(args) -> int:
    free = shutil.disk_usage(args.to).free
    if free < MIN_FREE_BYTES:
        # not enough disk on the target, ask infra to expand the volume
        return 8
    # download, verify, unpack happen here in the real service
    return exitcodes.OK
