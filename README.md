# fleetprobe

Lightweight status probe for the [dominus](https://github.com/ZachrielForever/legion)
game server host. Polls game server systemd user units on a one-minute timer
and publishes the results as JSON to the client share.

Bad data means bad visuals — the probe exists so dashboards never guess.

## How it works

- Checks `systemctl --user is-active` for each game server unit
- Writes `status.json` (name, online, port) to the client share
- Runs as a oneshot unit triggered by a systemd user timer (2min after boot, then every minute)
- No dependencies beyond the Python standard library

## Components

| File | Purpose |
| --- | --- |
| `fleetprobe.py` | The probe itself |
| `systemd/fleetprobe.service` | Oneshot unit definition |
| `systemd/fleetprobe.timer` | Timer trigger |
| `systemd/override.conf` | ExecStart redirect — see operational notes |

## Install

```bash
mkdir -p ~/.config/systemd/user
cp systemd/fleetprobe.service systemd/fleetprobe.timer ~/.config/systemd/user/
cp fleetprobe.py ~/tools/fleetprobe/
systemctl --user daemon-reload
systemctl --user enable --now fleetprobe.timer
