#!/usr/bin/env python3
import subprocess, json
from pathlib import Path

# name -> (systemd user unit, display port)
GAMES = {
    "UT99":        ("ut99.service",      7777),
    "UT2004":      ("ut2004.service",    8777),
    "Tribes 1":    ("tribes.service",   28001),
    "Tribes 2":    ("tribes2.service",   28000),
    "Quake II":    ("q2-dm.service",    27910),
    "Quake III":   ("q3a-dm.service",  27970),
    "Quake 4":     ("quake4.service",   28004),
    "Xonotic":     ("xonotic.service",  26000),
    "Red Eclipse": ("redeclipse.service", 28799),
    "Odamex":      ("odamex.service",   10666),
    "OpenRA":      ("openra-ra.service", 1234),
    "ET:Legacy":   ("etlegacy.service", 27960),
}

def is_active(unit):
    r = subprocess.run(
        ["systemctl", "--user", "is-active", unit],
        capture_output=True, text=True,
    )
    return r.stdout.strip() == "active"

def main():
    out = {}
    for name, (unit, port) in GAMES.items():
        out[name] = {"online": is_active(unit), "port": port}
    dest = Path("/home/zachriel/gameservers/clientshare/status.json")
    dest.write_text(json.dumps(out, indent=2))
    up = sum(1 for v in out.values() if v["online"])
    print(f"{up}/{len(out)} up, written {dest}")

if __name__ == "__main__":
    main()
