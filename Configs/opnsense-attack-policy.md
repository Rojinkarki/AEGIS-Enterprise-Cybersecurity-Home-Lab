# OPNsense ATTACK segmentation

## Recorded baseline

| Interface | Device | Attachment / address |
|---|---|---|
| WAN | `le0` | VirtualBox NAT |
| LAN | `le1` | Internal AEGIS-LAN, `10.50.0.1/24` |
| ATTACK | `em0` | Host-only transit, `10.60.10.1/24` |

| Alias | Type / members |
|---|---|
| `KALI_ATTACKER` | Host: `192.168.12.172` |
| `AEGIS_TARGETS` | Hosts: `10.50.0.10`, `10.50.0.20`, `10.50.0.30`, `10.50.0.40` |

The recorded ATTACK rule permits source `KALI_ATTACKER` to destination `AEGIS_TARGETS`, with logging enabled. Other inbound packets remain subject to the remaining rules and default deny. The full protocol/port settings and rule ordering were not exported, so this reference does not assert a verified least-port policy.

Gateway `KALI_RETURN_GW` points to `10.60.10.254` on ATTACK; route `192.168.12.172/32` selects it. [Routing details](network-routing.md) explain the Windows forwarding hop.

## Verification and evidence

- [ATTACK/LAN pass capture](../Screenshots/03-opnsense-attack-traffic.png): retains Kali source and DC01 destination with pass rows on ATTACK In and LAN Out.
- [Block capture](../Screenshots/04-opnsense-firewall-blocks.png): generic default-deny/state-violation rows. This is not a negative-test matrix for Kali or every alias boundary.
- [WAN capture](../Screenshots/05-opnsense-wan-traffic.png): separate firewall egress activity, not evidence that a particular Kali policy permits Internet access.

For a future policy audit, inspect alias members and rule order, then test an allowed source/target and an explicitly disallowed source/target in an owner-controlled network. Those negative tests were not run during this portfolio refresh.

## Security boundary

ATTACK is a transit network, not the enterprise LAN. The physical access network is outside AEGIS-LAN and the Windows forwarding host is part of the boundary. Enterprise hosts share `10.50.0.0/24`; their mutual traffic may not cross OPNsense. Suricata is IDS / alert-only, so firewall policy provides filtering. No WireGuard tunnel is used in the final path.
