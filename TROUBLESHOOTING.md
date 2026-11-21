# Troubleshooting & FAQ (`SM-P619`)

Common issues and quick fixes when building or flashing the One UI 7 LTE port (**AetherisOS 7.0**).

---

## 📱 Tablet & Flashing Issues

### 1. Stuck on the Samsung Logo (Bootloop)
* **Cause:** Data was not formatted before flashing, or the ROM was extracted on a Windows `C:\` folder instead of Ubuntu/WSL2.
* **Fix:**
  1. Force reboot into **LineageOS Recovery** (hold **Volume Down + Power** until the screen turns black, then immediately hold **Volume Up + Power**).
  2. Go to **Factory Reset** -> **Format data/factory reset** -> **Format data**.
  3. Re-sideload the ROM ZIP via `adb sideload`.

### 2. Odin Fails with `SECURE CHECK FAIL` or `Only official released binaries are allowed`
* **Cause:** Your bootloader is still locked, `KG State` is set to `Prenormal`, or you flashed a stock `CP` modem file after installing custom recovery.
* **Fix:**
  1. Flash full stock One UI 6.1 (`BL`, `AP`, `CP`, `CSC`) in Odin to recover.
  2. Boot into stock One UI 6.1, connect to Wi-Fi, and verify **OEM unlocking** is enabled in Developer Options (see [UNLOCK_BOOTLOADER.md](UNLOCK_BOOTLOADER.md)).
  3. **Never** flash `CP_*.tar.md5` in Odin after installing LineageOS Recovery.

### 3. ROM Boots, Wi-Fi Works, But SIM Card / LTE Has No Signal
* **Cause:** Missing RIL blob, APN settings, or SELinux denial blocking the modem.
* **Fix:**
  1. Check **Settings -> Connections -> Mobile networks -> Access Point Names** and add your carrier's APN manually if the list is empty.
  2. If your baseband shows **Unknown** in **Settings -> About tablet -> Software information**, pull a radio log over USB and open a GitHub Issue:
     ```bash
     adb logcat -b radio > radio.log
     ```

---

## 💻 PC & Ubuntu / WSL2 Issues

### 4. `wsl --install` Says "Elevated Permissions Required"
* **Fix:** You opened normal PowerShell instead of Administrator. Right-click the Start Menu and click **Terminal (Admin)** or **PowerShell (Admin)**, then run the command again.

### 5. `No such file or directory` When Copying Firmware from Downloads
* **Cause:** Your firmware files are saved in a different folder or drive (like `D:\` or Desktop) instead of `Downloads`.
* **Fix:** Move your `AP_*.tar.md5`, `CP_*.tar.md5`, and port `.zip` directly into your Windows **Downloads** folder, or drag-and-drop them into the `stock_raw` and `port_raw` folders manually.

### 6. How to Go Back to Official Samsung Stock Firmware
1. Download the official `SM-P619` One UI 6.1 firmware from SamFW.
2. Boot your tablet into **Download Mode** (`Volume Up + Volume Down` while plugging in USB).
3. Open Odin, load `BL`, `AP`, `CP`, and `CSC` into their matching slots (never check `Nand Erase`), and click **Start**.
