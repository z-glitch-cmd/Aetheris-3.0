# Aetheris 7.0 — AetherisOS 7.0 LTE Patcher (`SM-P619`)

A simple tool that adds working LTE mobile data, calls, and SMS to `SM-P613` (Wi-Fi) One UI 7 ports so they work as **AetherisOS 7.0** on the **Samsung Galaxy Tab S6 Lite 2022 LTE (`SM-P619`)**.

> ⚠️ **WARNING & DISCLAIMER**  
> **I am not responsible for bricked devices, dead SD cards, thermonuclear war, or you getting fired because the alarm app failed.**  
> **Your warranty is now void.** Unlocking your bootloader and flashing custom ROMs permanently voids your warranty and disables Samsung Knox apps (Samsung Pass, Secure Folder, Samsung Wallet). **YOU are choosing to make these changes.**

> 💻 **Important System Note**  
> This tool **only works on Linux (Ubuntu) or Windows (using Ubuntu WSL2)**.  
> Do **not** run this directly on a normal Windows `C:\` folder, or your tablet will bootloop.

---

## 📋 What You Need Before Starting

1. **Be on Official One UI 6.1 First:** Make sure your `SM-P619` tablet is already updated to the latest official Samsung One UI 6.1 firmware before unlocking and flashing anything.
2. **Stock One UI 6.1 Firmware (`SM-P619`):** Download the same One UI 6.1 firmware ZIP on your PC from [SamFW](https://samfw.com) (contains `AP_*.tar.md5` and `CP_*.tar.md5`).
3. **One UI 7 Port (`SM-P613`):** The Wi-Fi One UI 7 ROM ZIP you want to port.
4. **LineageOS Recovery (`gta4xlvelte`):** Download from the [LineageOS Wiki](https://lineageos.org).
5. **Android SDK Platform-Tools (`adb`):** Download from [Google Android Developers](https://android.com).
6. **Patched Odin (`v3.14.4_3B_PatcheD`):** Download from [XDA Forums](https://xdaforums.com) (Windows only, needed to flash LineageOS Recovery).
7. **PC Storage:** At least **45 GB of free space**.

---

## 🪟 Step 1: Windows Users Only

If you use **Windows**, install Ubuntu first:

1. Right-click the Start Menu and open **Terminal (Admin)** or **PowerShell (Admin)**.
2. Type this command and press Enter:
   ```powershell
   wsl --install -d Ubuntu
   ```
3. **Restart your PC** if asked.
4. Open **Ubuntu** from your Start Menu and create a username and password.
5. **Now follow the Linux Users steps below.**

---

## 🐧 Step 2: Linux Users (and Windows Users inside Ubuntu)

Copy and paste each command one by one into Ubuntu:

### 1. Install Required Tools
```bash
sudo apt update && sudo apt install -y git lz4 android-sdk-libsparse-utils android-sdk-platform-tools brotli p7zip-full python3 binutils
```

### 2. Download This Project
```bash
git clone https://github.com/z-glitch-cmd/Aetheris-3.0
```
```bash
cd Aetheris-3.0
```
> *(Note: If you see a `.gitignore` file in the folder, just ignore it—it keeps Git from uploading giant firmware files.)*

### 3. Create Folders
```bash
mkdir -p stock_raw stock_extracted port_raw port_extracted output
```

### 4. Put Your Firmware Files in the Folders
* **On Linux:** Put `AP_*.tar.md5` and `CP_*.tar.md5` inside `Aetheris-3.0/stock_raw/`, and your `SM-P613` One UI 7 ROM `.zip` inside `Aetheris-3.0/port_raw/`.
* **On Windows (WSL2):** Run these three commands to copy them from your Windows `Downloads` folder:
  ```bash
  cp /mnt/c/Users/*/Downloads/AP_*.tar.md5 stock_raw/
  ```
  ```bash
  cp /mnt/c/Users/*/Downloads/CP_*.tar.md5 stock_raw/
  ```
  ```bash
  cp /mnt/c/Users/*/Downloads/*.zip port_raw/
  ```

### 5. Unpack the Stock `SM-P619` Firmware
```bash
cd stock_raw
```
```bash
tar -xvf AP_*.tar.md5
```
```bash
tar -xvf CP_*.tar.md5
```
```bash
lz4 -d super.img.lz4 super.img
```
```bash
lz4 -d boot.img.lz4 ../stock_extracted/boot.img
```
```bash
lz4 -d dtbo.img.lz4 ../stock_extracted/dtbo.img
```
```bash
lz4 -d NON-HLOS.bin.lz4 ../stock_extracted/NON-HLOS.bin
```
```bash
simg2img super.img super_raw.img
```
```bash
cd ..
```

### 6. Unpack the `SM-P613` One UI 7 Port
```bash
7z x port_raw/*.zip -oport_extracted/
```

### 7. Run the LTE Patcher *(In Development)*
```bash
python3 patch_lte.py
```

---

## 📲 How to Flash on Your Tablet

> 🚨 **CRITICAL WARNINGS:**  
> 1. **Never flash the stock `CP_*.tar.md5` modem file in Odin after installing a custom recovery/ROM!** Doing so turns Secure Boot back on and blocks your tablet from booting. Stay on stock One UI 6.1 *before* flashing LineageOS Recovery so your modem stays intact.  
> 2. **Never check `Nand Erase` in Odin!** Doing so wipes your `EFS` partition (IMEI) and permanently breaks mobile data and calls.

1. **Install LineageOS Recovery:**
   * Boot your `SM-P619` into **Download Mode** (`Volume Up + Volume Down` while plugging in the USB cable).
   * Open **Patched Odin** on Windows, put `recovery.tar` in the **AP** slot, uncheck **Auto Reboot** in Options, and click **Start**.
   * Hold `Volume Down + Power` until the screen goes black, then immediately hold `Volume Up + Power` to enter **LineageOS Recovery**.
2. **Wipe Data:**
   * Tap **Factory Reset** -> **Format data/factory reset** -> **Format data**.
3. **Install AetherisOS 7.0:**
   * Tap **Apply Update** -> **Apply from ADB**.
   * On your PC (inside your `platform-tools` folder on Windows, or terminal on Linux), run:
     ```bash
     adb sideload output/AetherisOS-7.0-SM-P619.zip
     ```
4. **Reboot:**
   * Tap **Reboot system now** (the first boot takes 5–10 minutes).

---

## 📜 Credits

* **Your warranty is now void.** I am not responsible for bricked devices.
* **Credits:** Built on top of the community One UI 7 port for the Samsung Galaxy Tab S6 Lite 2022 (`gta4xlve`).
> 📖 **Guides:** [Supported Models](SUPPORTED_MODELS.md)
 • [Unlock Bootloader](UNLOCK_BOOTLOADER.md)
 • [Troubleshooting](TROUBLESHOOTING.md)

