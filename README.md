# Network Device Scanner

A Python command-line tool that lists the devices your computer can see on its local network, looks up their names, and flags any device it has not seen before.

## What it does

- Reads the computer's ARP table, which maps IP addresses to MAC addresses
- Filters out broadcast and multicast entries, which are not real devices
- Looks up a hostname for each device
- Saves every scan to a CSV history file with a timestamp
- Marks devices as NEW if their MAC address was not in any earlier scan

## Example output

```
IP address        MAC address         Name                    Status
--------------------------------------------------------------------
192.168.1.1       a4-83-e7-12-9b-01   router.home
192.168.1.14      3c-22-fb-0a-11-9e   unknown                 NEW

2 device(s) found, 1 new since earlier scans
```

## How to run it

Requires Windows and Python 3. No extra packages are needed.

```
python scanner.py
```

## How to run the tests

```
python -m unittest -v
```

## How it works

1. `get_arp_output` runs the Windows command `arp -a` using `subprocess`.
2. `parse_devices` uses a regular expression to pull out each IP and MAC address.
3. `is_real_device` removes broadcast (`ff-ff-ff-ff-ff-ff`) and multicast (`01-00-5e-...`) entries.
4. `get_hostname` does a reverse DNS lookup and returns `unknown` if there is no name.
5. `save_scan` appends the results to `scan_history.csv`, and `load_known_macs` reads that file on the next run to detect new devices.

## Limitations

- Windows only, because it relies on the output format of the Windows `arp` command.
- It only shows devices the computer has already communicated with. It does not actively scan the network.
- Many devices have no registered hostname, so they show as `unknown`.

## Responsible use

Only run this on a network you own or have permission to inspect. The history file is listed in `.gitignore` so that network details are not published.

## What I learned

- The difference between an IP address, which a network assigns and can change, and a MAC address, which is fixed to the device's hardware. This is why the scanner recognises devices by MAC address.
- How to run a system command from Python and turn its raw text output into structured data using a regular expression.
- Why code that depends on a network needs error handling. Hostname lookups often fail, so the program returns "unknown" and carries on.
- How to use Git and GitHub for version control, including fixing a rejected push by pulling remote changes first.
- Why some files should not be published. I used .gitignore to keep my network's scan history out of the repository.
- How to write unit tests that check functions with sample data, including an empty-input edge case.