# How to Unlock the Bootloader (`SM-P619`)

> ⚠️ **WARNING:**  
> * Unlocking your bootloader **erases all data** on your tablet. Back up everything important first.  
> * Unlocking permanently trips Samsung Knox (`0x1`), **voids your warranty**, and disables Samsung Pass, Secure Folder, and Samsung Wallet forever.

---

## Step 1: Turn On OEM Unlocking

1. Open **Settings** -> **About tablet** -> **Software information**.
2. Tap **Build number** 7 times until you see *"Developer mode has been turned on"*.
3. Go back to the main **Settings** menu and open **Developer options** at the very bottom.
4. Turn on **OEM unlocking** and **USB debugging**.
   *(If you don't see OEM unlocking, connect your tablet to Wi-Fi and wait a few minutes, or make sure the date/time is set to automatic.)*

---

## Step 2: Unlock in Download Mode

1. **Power off** your tablet completely.
2. Hold **Volume Up + Volume Down** at the same time and plug the USB cable into your PC.
3. When the blue/teal warning screen appears, **press and hold Volume Up** until the **Device Unlock Mode** screen pops up.
4. Press **Volume Up** once more to confirm unlocking.
5. Your tablet will wipe all data and reboot automatically.

---

## Step 3: Verify It Worked

1. Complete the quick initial setup (connect to Wi-Fi so Samsung registers the unlock status).
2. Enable **Developer options** again (tap **Build number** 7 times).
3. Check that **OEM unlocking** is turned **ON** and grayed out—your bootloader is now unlocked and ready for LineageOS Recovery.
