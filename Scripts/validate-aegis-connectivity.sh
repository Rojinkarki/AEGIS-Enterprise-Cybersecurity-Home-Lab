#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-10.50.0.10}"

echo "[+] Testing AEGIS target: $TARGET"
ping -c 3 "$TARGET"

echo "[+] Checking SMB reachability"
sudo nmap -Pn -p 445 "$TARGET"

echo "[+] Validation complete"
