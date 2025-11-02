# Pentizer

**Pentizer** is a helper script for adding and managing **Kali Linux** and **Parrot OS** repositories on a Debian-based distribution (e.g. Debian, Ubuntu, Linux Mint).

It automates:
- Backing up and restoring your APT sources  
- Adding Kali/Parrot repos with proper pinning rules  
- Importing their signing keys  
- Removing repos safely  

⚠️ **Warning:** Mixing repositories from different distributions can break your system if done incorrectly.  
This tool uses APT pinning to keep your base system safe, but you must still use it responsibly.

---

## Features
- **Backup/Restore** your APT sources (`/etc/apt/sources.list` + `/etc/apt/sources.list.d/`) into a tarball at `/etc/apt/backup/apt_sources_backup.tar.gz`.  
- **Add Kali repo** → Creates `/etc/apt/sources.list.d/kali.list` with low-priority pinning.  
- **Add Parrot repo** → Creates `/etc/apt/sources.list.d/parrot.list` with low-priority pinning.  
- **Pinning Rules** → Packages from Kali/Parrot will never overwrite your system automatically (`Pin-Priority: 100`).  
  You must explicitly install them with `-t`.  
- **Remove Repos** → Deletes the repo file, preferences, and GPG key.

---

## Usage
Run the script as **root**:

```bash
sudo python3 pentizer.py
```

You will see a menu:

```
=== Pentizer ===
1. Backup APT sources
2. Restore APT sources from backup
3. Add Kali repo (with pinning)
4. Remove Kali repo
5. Add Parrot repo (with pinning)
6. Remove Parrot repo
7. Exit
```

---

## Typical Workflow

1. **Backup first**
   ```bash
   1. Backup APT sources
   ```
   This creates a safe restore point at:
   ```
   /etc/apt/backup/apt_sources_backup.tar.gz
   ```

2. **Add a repo**
   ```bash
   3. Add Kali repo (with pinning)
   ```
   or
   ```bash
   5. Add Parrot repo (with pinning)
   ```

3. **Install tools explicitly**

   Always use `-t` to specify the target suite:

   ```bash
   sudo apt install -t kali-rolling nmap
   sudo apt install -t lory hydra
   ```

   > Note: Kali Linux uses suite name **kali-rolling**,  
   > Parrot OS 6 uses suite name **lory**.  
   > Pentizer automatically detects the correct suite and displays the right `-t` command after adding a repo.

4. **Remove repo when done (optional)**

   ```bash
   4. Remove Kali repo
   ```
   or
   ```bash
   6. Remove Parrot repo
   ```
   Then refresh:
   ```bash
   sudo apt update
   ```

5. **Restore if something breaks**
   ```bash
   2. Restore APT sources from backup
   ```

---

## Safety Notes
- Do **not** run `sudo apt upgrade` or `sudo apt full-upgrade` immediately after adding Kali/Parrot without understanding what will be upgraded.  
- With `Pin-Priority: 100`, your base system won’t automatically upgrade to Kali/Parrot packages.  
  However, if you install something without `-t`, APT might still pull dependencies from them.  
- This tool is intended for installing **specific security tools**, *not* for turning your Debian/Ubuntu/Mint system into Kali or Parrot.  
- If your package system becomes unstable, use the restore option to roll back your sources.

---

## Requirements
- Debian-based system (Debian, Ubuntu, Linux Mint, etc.)
- Python 3
- Root privileges (`sudo`)
- `tar`, `wget`, and `gpg` installed

---

## Compatibility
✅ Tested and working on **Linux Mint 22.2 (Zara)**  
⚠️ Use at your own risk — the author is **not responsible** for any damage, data loss, or package corruption.

---

## Disclaimer
This tool is provided **as-is**.  
Adding foreign repositories can break your system if misused.  
Always back up your data before experimenting.
