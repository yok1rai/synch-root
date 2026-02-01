#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

# Configuration
SCRIPT_NAME = "sync-root"
SOURCE = Path("bin") / SCRIPT_NAME
DEST_DIR = Path("/usr/local/bin")
DEST = DEST_DIR / SCRIPT_NAME

# Safety check
if Path("/").resolve() == SOURCE.resolve().parent:
    print("Error: Source appears to be in root filesystem. Aborting for safety.")
    sys.exit(1)

# Ensure source exists
if not SOURCE.exists():
    print(f"Error: {SOURCE} not found")
    sys.exit(1)

# Ensure destination directory exists
DEST_DIR.mkdir(parents=True, exist_ok=True)

# Copy script and set permissions
try:
    shutil.copy2(SOURCE, DEST)
    DEST.chmod(0o755)
    print(f"{SCRIPT_NAME} installed to {DEST}")
except PermissionError:
    print("Error: Permission denied. Try running with root priviliges")
    sys.exit(1)

print(f"Installation complete. You can now run '{SCRIPT_NAME}' from anywhere.")
