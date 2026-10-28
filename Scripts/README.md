# Validation scripts

These helpers contain no credentials and do not change lab routing or generate authentication attempts.

## Physical Kali connectivity

```bash
bash Scripts/validate-aegis-connectivity.sh
# Optional: select one of the four explicit AEGIS hosts.
bash Scripts/validate-aegis-connectivity.sh 10.50.0.30
```

Run locally on the authorized physical Kali system with `ip`, `ping`, `nmap`, and sudo available. The script accepts only DC01/SOC01/WS01/WAZUH01 addresses, checks the expected Windows next hop, tries ICMP, and runs the same top-100-port SYN scan used for the Nmap evidence. Sudo is used only for the SYN scan. ICMP failure is reported but does not prevent TCP inspection.

A completed scan is not a guarantee of application health or successful authentication. Review states and open ports; the script does not label a completed scan as an all-controls pass.

## Windows route inspection

```powershell
.\Scripts\collect-windows-lab-status.ps1
```

Read-only helper for the Windows virtualization host. Reports relevant addresses, IPv4 forwarding, and active/persistent AEGIS routes. It does not export credentials, modify interfaces, or create firewall rules. Compare results with [Configs/network-routing.md](../Configs/network-routing.md).

## Repository hygiene

```text
python Scripts/check-repository.py
python Scripts/check-repository.py --history
```

Requires Python 3 and Git, with no third-party packages. Checks local Markdown links, evidence hashes, duplicate images, excluded artifact types, and common secret patterns without printing matched values. `--history` also checks reachable historical text blobs. This is a focused hygiene check rather than a guarantee that all possible secrets are detected; screenshots also require visual review.

Syntax checks and controlled command-stub checks were performed during the portfolio refresh. The scripts were not run against the live range in that refresh.
