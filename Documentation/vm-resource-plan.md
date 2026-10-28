# AEGIS v1 VM resource plan

**Status: AEGIS v1.0 complete.** Recorded host: Windows 11 Home, AMD Ryzen 7 8845HS (8 cores / 16 threads), 32 GB RAM, NVIDIA RTX 4060, Oracle VirtualBox. Available storage at project start was approximately 500 GB.

## VM allocations

| VM | Platform | RAM | vCPU | Dynamic disk | Role |
|---|---|---:|---:|---:|---|
| OPNsense-FW | OPNsense 26.7.3_11 | 4 GB | 2 | 25 GB | Gateway, WAN/LAN/ATTACK, Suricata IDS |
| DC01 | Windows Server 2025 Standard Evaluation | 4 GB | 2 | 60 GB | AD DS, DNS, Group Policy, endpoint agents |
| WS01 | Windows 11 Enterprise Evaluation | 6 GB | 4 | 80 GB | Domain workstation, Sysmon, endpoint agents |
| SOC01 | Ubuntu Server 24.04 LTS | 8 GB | 4 | 100 GB | Splunk Enterprise |
| WAZUH01 | Ubuntu Server 24.04 LTS | 8 GB | 4 | 80 GB | Wazuh manager, indexer and dashboard |

Configured disk capacity totals 345 GB before snapshot growth. Dynamic disks consume storage as data is written; snapshots and installation media require additional space. Physical Kali is a separate laptop and does not consume this host's VM allocation.

## Workload profiles

| Profile | Running VMs | Allocated guest RAM |
|---|---|---:|
| Network / identity | OPNsense + DC01 + WS01 | 14 GB |
| Splunk investigation | OPNsense + DC01 + WS01 + SOC01 | 22 GB |
| Wazuh investigation | OPNsense + DC01 + WS01 + WAZUH01 | 22 GB |
| All systems | All five VMs | 30 GB |

Normal operation uses the relevant 14 or 22 GB profile. A 22 GB profile leaves approximately 10 GB before host and VirtualBox overhead; running all systems leaves too little headroom on a 32 GB host. Splunk and Wazuh validation can therefore occur in separate sessions rather than simultaneously.

## Final networking

Enterprise VMs use AEGIS-LAN with gateway `10.50.0.1` and DNS `10.50.0.10`. Temporary installation-only NAT adapters were removed in the final build. OPNsense provides:

| Interface | Attachment | Address |
|---|---|---|
| WAN / le0 | VirtualBox NAT | VirtualBox-managed |
| LAN / le1 | Internal AEGIS-LAN | `10.50.0.1/24` |
| ATTACK / em0 | Host-only transit | `10.60.10.1/24` |

The Windows host-only side is `10.60.10.254/24`; physical Kali reaches it through Windows IPv4 forwarding. See [architecture.md](architecture.md) and [network-plan.txt](network-plan.txt).

## Recovery points

The baseline records intermediate milestones for AD health, Group Policy, forwarder integration, Splunk detections, Wazuh integration, and OPNsense/Suricata. Final v1 recovery points supersede those build stages for the completed portfolio baseline:

- `OPNsense-AEGIS-v1-Final`
- `DC01-AEGIS-v1-Final`
- `WS01-AEGIS-v1-Final`
- `SOC01-AEGIS-v1-Final`
- `WAZUH01-AEGIS-v1-Final`

Snapshots and VM disks remain local and outside Git. Inventory and restore operations were not repeated during the repository refresh; see [validation.md](validation.md).
