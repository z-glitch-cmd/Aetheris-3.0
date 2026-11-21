#!/usr/bin/env python3
"""
Aetheris 7.0 — SM-P619 (gta4xlvelte) AetherisOS 7.0 LTE Port Patcher
Interactive Terminal UI using Python's built-in curses library.
"""

import curses
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STOCK_RAW = BASE_DIR / "stock_raw"
STOCK_EXT = BASE_DIR / "stock_extracted"
PORT_EXT = BASE_DIR / "port_extracted"
OUTPUT_DIR = BASE_DIR / "output"

LTE_KEYWORDS = (
    "ril", "qcril", "sec-ril", "radio", "modem", "ims",
    "telephony", "qmi", "diag", "rmnet", "ipa", "netmgr"
)


def ensure_dirs():
    for folder in [STOCK_RAW, STOCK_EXT, PORT_EXT, OUTPUT_DIR]:
        folder.mkdir(parents=True, exist_ok=True)


def get_status_summary():
    modem_ok = (STOCK_EXT / "NON-HLOS.bin").exists()
    dtbo_ok = (STOCK_EXT / "dtbo.img").exists()
    boot_ok = (STOCK_EXT / "boot.img").exists()
    port_ok = any(PORT_EXT.iterdir()) if PORT_EXT.exists() else False
    vendor_ok = (STOCK_EXT / "vendor").exists() and (PORT_EXT / "vendor").exists()
    return {
        "Modem (NON-HLOS.bin)": "READY" if modem_ok else "MISSING",
        "Device Tree (dtbo.img)": "READY" if dtbo_ok else "MISSING",
        "Kernel (boot.img)": "READY" if boot_ok else "MISSING",
        "Base SM-P613 7.0 Port": "READY" if port_ok else "EMPTY",
        "Unpacked vendor/": "READY" if vendor_ok else "PENDING",
    }


def run_full_audit():
    lines = ["=== WORKSPACE & STOCK SM-P619 CHECK ==="]
    for fname in ["NON-HLOS.bin", "dtbo.img", "boot.img"]:
        fpath = STOCK_EXT / fname
        if fpath.exists():
            size_mb = fpath.stat().st_size / (1024 * 1024)
            lines.append(f"[OK] {fname} ({size_mb:.1f} MB)")
        else:
            lines.append(f"[MISSING] {fname} — run Step 5 in README first.")

    lines.append("")
    lines.append("=== BASE SM-P613 ONE UI 7 PORT CONTENTS ===")
    items = sorted(PORT_EXT.iterdir()) if PORT_EXT.exists() else []
    if not items:
        lines.append("[MISSING] port_extracted/ is empty — run Step 6 in README first.")
    else:
        for item in items:
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                lines.append(f"  File: {item.name} ({size_mb:.1f} MB)")
            else:
                lines.append(f"  Dir:  {item.name}/")

    lines.append("")
    lines.append("=== VENDOR RIL / LTE BLOB SCAN ===")
    stock_vendor = STOCK_EXT / "vendor"
    port_vendor = PORT_EXT / "vendor"

    if not stock_vendor.exists() or not port_vendor.exists():
        lines.append("[INFO] Unpacked vendor/ folders not detected yet.")
        lines.append("       Extract vendor.img into stock_extracted/vendor and port_extracted/vendor,")
        lines.append("       then run this scan again.")
    else:
        stock_ril_files = set()
        for root, _, files in os.walk(stock_vendor):
            for f in files:
                if any(k in f.lower() for k in LTE_KEYWORDS):
                    rel_path = Path(root).relative_to(stock_vendor) / f
                    stock_ril_files.add(str(rel_path))

        missing_in_port = [
            rel_str for rel_str in sorted(stock_ril_files)
            if not (port_vendor / rel_str).exists()
        ]

        report_path = OUTPUT_DIR / "missing_lte_blobs.txt"
        with open(report_path, "w", encoding="utf-8") as out:
            for item in missing_in_port:
                out.write(item + "\n")

        lines.append(f"[DONE] Found {len(missing_in_port)} missing SM-P619 LTE/RIL files.")
        lines.append("       Saved full list to: output/missing_lte_blobs.txt")

    return lines


def view_missing_report():
    report_path = OUTPUT_DIR / "missing_lte_blobs.txt"
    if not report_path.exists():
        return [
            "[INFO] output/missing_lte_blobs.txt has not been generated yet.",
            "       Run '1. Run Full Firmware & LTE Audit' first once vendor/ is unpacked."
        ]
    content = report_path.read_text(encoding="utf-8").splitlines()
    if not content:
        return ["[OK] No missing LTE blobs listed in missing_lte_blobs.txt."]
    return [f"=== MISSING LTE BLOBS ({len(content)} files) ==="] + content[:35]


def draw_ui(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)

    ensure_dirs()
    menu_items = [
        "1. Run Full Firmware & LTE Audit",
        "2. View Missing LTE Blobs Report",
        "3. Refresh Status Dashboard",
        "4. Exit",
    ]
    selected = 0
    output_lines = [
        "Welcome to Aetheris 7.0 (AetherisOS 7.0) LTE Port Patcher.",
        "Use UP/DOWN arrows to choose an option and press ENTER.",
    ]

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Header
        title = " AETHERIS 7.0 — AETHERISOS 7.0 LTE PATCHER (SM-P619) "
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(1, 2, title[: width - 4])
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Status Box
        stdscr.addstr(3, 2, "Workspace Status:")
        status = get_status_summary()
        row = 4
        for label, state in status.items():
            stdscr.addstr(row, 4, f"{label:<24}: ")
            color = curses.color_pair(2) if state == "READY" else curses.color_pair(3)
            stdscr.attron(color | curses.A_BOLD)
            stdscr.addstr(state)
            stdscr.attroff(color | curses.A_BOLD)
            row += 1

        # Menu
        row += 1
        stdscr.addstr(row, 2, "Actions:")
        row += 1
        for idx, item in enumerate(menu_items):
            if idx == selected:
                stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
                stdscr.addstr(row, 4, f" > {item} ")
                stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            else:
                stdscr.addstr(row, 4, f"   {item} ")
            row += 1

        # Output Log Pane
        row += 1
        stdscr.addstr(row, 2, "-" * min(60, width - 4))
        row += 1
        for line in output_lines:
            if row >= height - 1:
                break
            stdscr.addstr(row, 2, line[: width - 4])
            row += 1

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(menu_items) - 1:
            selected += 1
        elif key in (curses.KEY_ENTER, 10, 13):
            if selected == 0:
                output_lines = run_full_audit()
            elif selected == 1:
                output_lines = view_missing_report()
            elif selected == 2:
                output_lines = ["[OK] Status dashboard refreshed."]
            elif selected == 3:
                break


if __name__ == "__main__":
    curses.wrapper(draw_ui)
