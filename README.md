# Pentizer  

Pentizer is a helper script for adding and managing **Kali Linux** and **Parrot OS** repositories on a Debian-based distribution (e.g. Debian, Ubuntu, Linux Mint).  

It automates:  
- Backing up and restoring your APT sources  
- Adding Kali/Parrot repos with proper pinning rules  
- Importing their signing keys  
- Removing repos safely  

⚠️ **Warning**: Mixing repositories from different distributions can break your system if done incorrectly. This tool uses *APT pinning* to keep your base system safe, but you must still use it responsibly.  

---

## Features  
- **Backup/Restore** your APT sources (`/etc/apt/sources.list` + `/etc/apt/sources.list.d/`) into a tarball at `/etc/apt/backup/apt_sources_backup.tar.gz`.  
- **Add Kali repo** → Creates `/etc/apt/sources.list.d/kali.list` with low priority pinning.  
- **Add Parrot repo** → Creates `/etc/apt/sources.list.d/parrot.list` with low priority pinning.  
- **Pinning Rules** → Packages from Kali/Parrot will never overwrite your system automatically (`Pin-Priority: 100`). You must explicitly install them with `-t`.  
- **Remove Repos** → Deletes the repo file, preferences, and GPG key.  

---

## Usage  

Run the script as **root** (sudo):  

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

### Typical workflow  

1. **Backup first**  
   ```
   1. Backup APT sources
   ```
   This creates a safe restore point at `/etc/apt/backup/apt_sources_backup.tar.gz`.  

2. **Add a repo**  
   ```
   3. Add Kali repo (with pinning)
   ```
   or  
   ```
   5. Add Parrot repo (with pinning)
   ```

3. **Install tools explicitly**  
   Always use `-t` to specify the repo target. Example:  
   ```bash
   sudo apt install -t kali-rolling nmap
   sudo apt install -t parrot hydra
   ```

4. **Remove repo when done (optional)**  
   ```
   4. Remove Kali repo
   6. Remove Parrot repo
   ```

5. **Restore if broken**  
   If your sources get messed up, run:  
   ```
   2. Restore APT sources from backup
   ```

---

## Safety Notes  

- Do **not** run `sudo apt upgrade` or `sudo apt full-upgrade` immediately after adding Kali/Parrot without understanding what will be upgraded.  
- With pinning set to `100`, your base system will not auto-upgrade to Kali/Parrot packages — but if you manually install something with `apt install` (without `-t`), APT might still try to resolve dependencies from them.  
- This tool is intended for **installing a few specific security tools**, not for turning your Debian/Ubuntu/Mint system into a full Kali or Parrot OS.  
- If your package system becomes unstable, use the restore option to roll back your sources.  

---

## Requirements  

- Debian-based system (Debian, Ubuntu, Linux Mint, etc.)  
- Python 3  
- Root privileges (`sudo`)  
- `tar`, `wget`, and `gpg` installed  

---

## Disclaimer  

This tool is provided **as-is**. Adding foreign repositories can break your system if misused.  
Use at your own risk. Always back up your important data before experimenting.  
