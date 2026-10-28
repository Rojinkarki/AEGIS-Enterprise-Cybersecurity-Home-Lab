#!/usr/bin/env bash
set -euo pipefail

if (( $# > 1 )); then
  echo "Usage: $0 [10.50.0.10|10.50.0.20|10.50.0.30|10.50.0.40]" >&2
  exit 2
fi

TARGET="${1:-10.50.0.10}"
case "$TARGET" in
  10.50.0.10|10.50.0.20|10.50.0.30|10.50.0.40) ;;
  *) echo "Target must be one of the four authorized AEGIS hosts." >&2; exit 2 ;;
esac

for dependency in ip ping nmap sudo; do
  command -v "$dependency" >/dev/null || {
    echo "Missing dependency: $dependency" >&2
    exit 1
  }
done

echo "[+] Inspecting the route to $TARGET"
route_result="$(ip route get "$TARGET")"
printf '%s\n' "$route_result"
if [[ " $route_result " != *" via 192.168.12.180 "* ]]; then
  echo "Expected the physical Kali route via Windows 192.168.12.180; stopping." >&2
  exit 1
fi

echo "[+] Trying ICMP (endpoint policy may block it)"
if ! ping -c 3 -W 2 "$TARGET"; then
  echo "[!] No ICMP reply; continuing with TCP inspection."
fi

echo "[+] Running the authorized top-100-port SYN scan"
sudo nmap -Pn -sS --top-ports 100 "$TARGET"
echo "[+] Scan finished. Review port states and correlate OPNsense ATTACK logs."
