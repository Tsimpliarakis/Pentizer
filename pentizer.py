#!/usr/bin/env python3
import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path

# Detect if colors should be enabled
USE_COLOR = sys.stdout.isatty()

def c(code):
    return code if USE_COLOR else ""

# ANSI escape codes for colors
COLORS = {
    "GREEN": c("\033[92m"),
    "YELLOW": c("\033[93m"),
    "RED": c("\033[91m"),
    "CYAN": c("\033[96m"),
    "RESET": c("\033[0m"),
    "BOLD": c("\033[1m")
}

# Paths
APT_DIR = Path("/etc/apt/sources.list.d")
PREF_DIR = Path("/etc/apt/preferences.d")
BACKUP_FILE = Path("/etc/apt/sources.list.bak")

# Repo definitions
REPOS = {
    "kali": {
        "repo": "deb http://http.kali.org/kali kali-rolling main non-free contrib",
        "pref": """Package: *
Pin: release n=kali-rolling
Pin-Priority: 100
""",
        "key_url": "https://archive.kali.org/archive-key.asc",
        "key_file": "/etc/apt/trusted.gpg.d/kali.gpg"
    },
    "parrot": {
        "repo": "deb http://deb.parrot.sh/parrot parrot main contrib non-free",
        "pref": """Package: *
Pin: release n=parrot
Pin-Priority: 100
""",
        "key_url": "https://deb.parrot.sh/parrot/mirrors/parrot.gpg",
        "key_file": "/etc/apt/trusted.gpg.d/parrot.gpg"
    }
}

def backup_sources():
    """Backup original sources.list"""
    sources = Path("/etc/apt/sources.list")
    if sources.exists() and not BACKUP_FILE.exists():
        shutil.copy2(sources, BACKUP_FILE)
        print(COLORS["GREEN"] + f"Backup created: {BACKUP_FILE}" + COLORS["RESET"])
    else:
        print(COLORS["YELLOW"] + "Backup already exists or sources.list not found." + COLORS["RESET"])

def restore_sources():
    """Restore sources.list from backup"""
    if BACKUP_FILE.exists():
        shutil.copy2(BACKUP_FILE, "/etc/apt/sources.list")
        print(COLORS["GREEN"] + "sources.list restored from backup." + COLORS["RESET"])
    else:
        print(COLORS["RED"] + "No backup found." + COLORS["RESET"])

def import_key(name):
    """Download and install repo signing key"""
    key_url = REPOS[name]["key_url"]
    key_file = REPOS[name]["key_file"]

    try:
        wget = subprocess.run(
            ["wget", "-qO", "-", key_url],
            check=True,
            stdout=subprocess.PIPE
        )
        with open(key_file, "wb") as out:
            subprocess.run(
                ["gpg", "--dearmor"],
                input=wget.stdout,
                check=True,
                stdout=out
            )
        print(COLORS["GREEN"] + f"{name} signing key installed at {key_file}" + COLORS["RESET"])
    except subprocess.CalledProcessError:
        print(COLORS["RED"] + f"Failed to download {name} key." + COLORS["RESET"])
    except Exception as e:
        print(COLORS["RED"] + f"Error importing {name} key: {e}" + COLORS["RESET"])

def add_repo(name):
    """Add repo, preferences, and signing key"""
    repo_file = APT_DIR / f"{name}.list"
    pref_file = PREF_DIR / f"{name}.pref"

    if repo_file.exists():
        print(COLORS["YELLOW"] + f"{name} repo already exists." + COLORS["RESET"])
        return

    if not APT_DIR.exists() or not PREF_DIR.exists():
        print(COLORS["RED"] + "APT directories missing. Are you sure this is a Debian-based system?" + COLORS["RESET"])
        return

    # Write repo file
    with open(repo_file, "w") as f:
        f.write(REPOS[name]["repo"] + "\n")
    print(COLORS["GREEN"] + f"{name} repo added at {repo_file}" + COLORS["RESET"])

    # Write preferences file
    with open(pref_file, "w") as f:
        f.write(REPOS[name]["pref"])
    print(COLORS["GREEN"] + f"{name} pinning rules added at {pref_file}" + COLORS["RESET"])

    # Import GPG key
    import_key(name)

    run_update()
    print(COLORS["CYAN"] + f"To install packages from {name}, use:" + COLORS["RESET"])
    print(COLORS["CYAN"] + f"  sudo apt install -t {name} <package>\n" + COLORS["RESET"])

def remove_repo(name):
    """Remove repo, preferences, and signing key"""
    repo_file = APT_DIR / f"{name}.list"
    pref_file = PREF_DIR / f"{name}.pref"
    key_file = Path(REPOS[name]["key_file"])

    if repo_file.exists():
        repo_file.unlink()
        print(COLORS["GREEN"] + f"{name} repo removed." + COLORS["RESET"])
    if pref_file.exists():
        pref_file.unlink()
        print(COLORS["GREEN"] + f"{name} pinning rules removed." + COLORS["RESET"])
    if key_file.exists():
        key_file.unlink()
        print(COLORS["GREEN"] + f"{name} signing key removed." + COLORS["RESET"])

    run_update()

def run_update():
    """Run apt-get update"""
    try:
        subprocess.run(["apt-get", "update"], check=True)
        print(COLORS["GREEN"] + "apt-get update successful." + COLORS["RESET"])
    except subprocess.CalledProcessError:
        print(COLORS["RED"] + "apt-get update failed. Check your internet or repo config." + COLORS["RESET"])

def menu():
    print(COLORS["BOLD"] + "\n=== Pentizer ===" + COLORS["RESET"])
    print("1. Backup sources.list")
    print("2. Restore sources.list from backup")
    print("3. Add Kali repo (with pinning)")
    print("4. Remove Kali repo")
    print("5. Add Parrot repo (with pinning)")
    print("6. Remove Parrot repo")
    print("7. Exit")

    choice = input("Select an option: ").strip()

    if choice == "1":
        backup_sources()
    elif choice == "2":
        restore_sources()
    elif choice == "3":
        add_repo("kali")
    elif choice == "4":
        remove_repo("kali")
    elif choice == "5":
        add_repo("parrot")
    elif choice == "6":
        remove_repo("parrot")
    elif choice == "7":
        exit(0)
    else:
        print(COLORS["RED"] + "Invalid choice." + COLORS["RESET"])

if __name__ == "__main__":
    if platform.system() != "Linux" or not Path("/etc/debian_version").exists():
        print(COLORS["RED"] + "Run this script in a Debian-based Linux environment." + COLORS["RESET"])
        exit(1)

    if os.geteuid() != 0:
        print(COLORS["RED"] + "Run this script with sudo/root privileges." + COLORS["RESET"])
        exit(1)

    while True:
        menu()
