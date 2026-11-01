import os

BUCKET = os.environ.get("BACKUP_BUCKET", "smc-prod-backups")
RETENTION_DAYS = 14
LOCK_FILE = "/var/run/backup.lock"
DEFAULT_CONFIG_PATH = "/etc/backup/config.toml"
