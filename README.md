# Network Device Scanner

A Python command-line tool that shows which devices your computer can see on its local network, and flags any device it has not seen before.

I built it to learn how devices find each other on a network, and to have a quick way of spotting an unfamiliar device.

## Features

- Reads the computer's ARP table, which maps IP addresses to MAC addresses
- Filters out broadcast and multicast entries, which are not real devices
- Looks up a hostname for each device and handles lookups that fail
- Saves every scan to a CSV history file with a timestamp
- Marks a device as NEW if its MAC address was not in any earlier scan
- Includes unit tests for the parsing and filtering logic

## Example output

```
IP address        MAC address         Name                    Status
--------------------------------------------------------------------
192.168.1.1       a4-83-e7-12-9b-01   router.home
192.168.1.14      3c-22-fb-0a-11-9e   unknown                 NEW

2 device(s) found, 1 new since earlier scans
```

The addresses above are made up for illustration.

## Getting started

Requires Windows and Python 3. No extra packages are needed.

```
git clone https://github.com/foysalbinislam/network-device-scanner.git
cd network-device-scanner
python scanner.py
```

Run it a second time to see the new-device detection: devices from the first scan are no longer marked NEW.

## Running the tests

```
python -m unittest -v
```

## Project files

| File | Purpose |
| --- | --- |
| `scanner.py` | The scanner itself |
| `test_scanner.py` | Unit tests for parsing and filtering |
| `.gitignore` | Keeps the scan history and cache files out of the repository |

## How it works

1. `get_arp_output` runs the Windows command `arp -a` using `subprocess`.
2. `parse_devices` uses a regular expression to pull out each IP and MAC address.
3. `is_real_device` removes broadcast (`ff-ff-ff-ff-ff-ff`) and multicast (`01-00-5e-...`) entries.
4. `get_hostname` does a reverse DNS lookup and returns `unknown` if there is no name.
5. `load_known_macs` reads `scan_history.csv` to find MAC addresses from earlier scans.
6. `save_scan` appends the latest results to that file with a timestamp.

Devices are recognised by MAC address, not IP address, because an IP address can be reassigned to a different device while a MAC address stays with the hardware.

## Built with

Python 3 and its standard library only: `subprocess`, `re`, `socket`, `csv`, `datetime`, `pathlib` and `unittest`.

## Limitations

- Windows only, because it relies on the output format of the Windows `arp` command.
- It only shows devices the computer has already communicated with. It does not actively scan the network.
- Many devices have no registered hostname, so they show as `unknown`.
- On managed networks that isolate users from each other, such as university networks, only the routers are visible.

## Planned improvements

- An optional active scan that pings each address first, for use on a home network
- Showing the device manufacturer, looked up from the first half of the MAC address
- Support for macOS and Linux
- Command-line options, such as choosing where the history file is saved

## Responsible use

Only run this on a network you own or have permission to inspect. The scan history is listed in `.gitignore` so that network details are not published.

## What I learned

- The difference between an IP address, which a network assigns and can change, and a MAC address, which is fixed to the device's hardware.
- How to run a system command from Python and turn its raw text output into structured data using a regular expression.
- Why code that depends on a network needs error handling. Hostname lookups often fail, so the program returns "unknown" and carries on.
- How to use Git and GitHub for version control, including fixing a rejected push by pulling remote changes first.
- Why some files should not be published, and how to use `.gitignore` to keep them out of a repository.
- How to write unit tests that check functions with sample data, including an empty-input edge case.
