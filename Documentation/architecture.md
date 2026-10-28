# AEGIS v1 architecture

**Status: AEGIS v1.0 complete.** This is the final recorded build, with evidence qualifications in [validation.md](validation.md).

## Network zones

| Zone | Network | Purpose |
|---|---|---|
| Physical access | `192.168.12.0/24` | Kali and Windows host Wi-Fi |
| ATTACK transit | `10.60.10.0/24` | VirtualBox host-only link from Windows to OPNsense |
| AEGIS-LAN | `10.50.0.0/24` | VirtualBox internal enterprise network |
| WAN | VirtualBox NAT | Internet egress through OPNsense |

```text
Physical Kali 192.168.12.172
  -> Windows Wi-Fi 192.168.12.180
  -> Windows IPv4 forwarding / host-only 10.60.10.254
  -> OPNsense ATTACK em0 10.60.10.1
  -> scoped, logged firewall policy
  -> OPNsense LAN le1 10.50.0.1
  -> AEGIS-LAN targets

AEGIS-LAN -> OPNsense WAN le0 -> VirtualBox NAT -> Internet
```

## Systems

| System | Address | Platform / role |
|---|---|---|
| OPNsense-FW | LAN `10.50.0.1/24`; ATTACK `10.60.10.1/24` | OPNsense 26.7.3_11, firewall, Suricata IDS |
| DC01 | `10.50.0.10/24` | Windows Server 2025, AD DS, DNS, Group Policy |
| SOC01 | `10.50.0.20/24` | Ubuntu Server 24.04 LTS, Splunk Enterprise 10.4.2 |
| WS01 | `10.50.0.30/24` | Windows 11 Enterprise, domain workstation, Sysmon |
| WAZUH01 | `10.50.0.40/24` | Ubuntu Server 24.04 LTS, Wazuh 4.14.7 |

Domain: `corp.aegis.test`. Enterprise DNS: DC01. Default gateway: OPNsense LAN. Installation-only secondary NAT adapters were removed from enterprise VMs in the recorded final build.

## Routing and segmentation

| Router | Persistent destination | Next hop |
|---|---|---|
| Kali | `10.50.0.0/24` | `192.168.12.180` |
| Windows | `10.50.0.0/24` | `10.60.10.1` |
| OPNsense | `192.168.12.172/32` | `10.60.10.254` via `KALI_RETURN_GW` |

Windows forwards IPv4 between Wi-Fi and host-only. OPNsense's host return route prevents Kali replies taking the WAN default route. No source NAT is applied to the internal Kali-to-DC01 path: retained logs show source `192.168.12.172`. The build record reports successful checks after host and VM restarts.

On ATTACK, `KALI_ATTACKER` contains Kali's single address and `AEGIS_TARGETS` contains DC01, SOC01, WS01, and WAZUH01. The recorded pass rule uses those aliases with logging enabled. Other inbound traffic is subject to remaining rules and default deny. See [policy details](../Configs/opnsense-attack-policy.md) for the limits of the retained negative-test evidence.

The earlier WireGuard path was disabled and is outside the final v1 design. No tunnel keys or appliance exports are published.

## Telemetry

```text
DC01 Security events -----+--> Splunk Universal Forwarder --> SOC01 --> SPL detections
WS01 Security / Sysmon ---+

DC01 / WS01 Wazuh agents ----> WAZUH01 --> alerts / threat hunting

Traffic crossing OPNsense ---> firewall Live View
                            -> Suricata IDS / ET Open --> network alerts
```

Suricata is deployed in IDS / alert-only mode, not inline prevention. Firewall-local inspection does not see every exchange between VMs on the same subnet. The final screenshot set does not establish the complete IDS interface selection; prior SID validation and the unsuccessful latest capture attempt are documented separately.

## Boundaries and recovery

AEGIS has NAT egress and a routed physical entry point. The Windows forwarding host is part of the trust boundary. There is no direct Kali bridge into the enterprise subnet, and no v1 claim of per-host microsegmentation or production hardening.

Recorded snapshots: `OPNsense-AEGIS-v1-Final`, `DC01-AEGIS-v1-Final`, `WS01-AEGIS-v1-Final`, `SOC01-AEGIS-v1-Final`, `WAZUH01-AEGIS-v1-Final`. They remain local VirtualBox artifacts. See [milestones](progress-log.md) and [resource profiles](vm-resource-plan.md).
