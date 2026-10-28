# Persistent physical Kali routing

## Recorded final values

| Component | Address |
|---|---|
| Kali | `192.168.12.172/24` |
| Windows Wi-Fi | `192.168.12.180/24` |
| Windows VirtualBox host-only | `10.60.10.254/24` |
| OPNsense ATTACK | `10.60.10.1/24` |
| OPNsense LAN | `10.50.0.1/24` |

| System | Destination | Next hop |
|---|---|---|
| Kali | `10.50.0.0/24` | `192.168.12.180` |
| Windows | `10.50.0.0/24` | `10.60.10.1` |
| OPNsense | `192.168.12.172/32` | `10.60.10.254` |

The completed build records persistent Windows IPv4 forwarding and successful reachability after host/VM restarts. The repository refresh did not change or inspect live networking. Reserve the physical addresses or update all dependent routes if DHCP assignments change.

## Kali persistence example

The following is a reconstruction example for a NetworkManager-managed connection. The original connection name is not retained. Select the connection used to reach the Windows Wi-Fi address; do not export the full connection profile because it can include Wi-Fi credentials.

```bash
nmcli -f NAME,DEVICE connection show --active
# Replace the example value with the existing connection name.
AEGIS_CONNECTION='your-existing-connection-name'
sudo nmcli connection modify "$AEGIS_CONNECTION" +ipv4.routes '10.50.0.0/24 192.168.12.180'
# Reactivating the connection may briefly interrupt it; run locally on Kali.
sudo nmcli connection up "$AEGIS_CONNECTION"
nmcli -g ipv4.routes connection show "$AEGIS_CONNECTION"
ip route get 10.50.0.10
```

Add the route once after checking existing values. `ip route add` alone changes runtime state and is not the persistence mechanism shown here. NetworkManager saves connection changes; see the [official nmcli reference](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nmcli.html) and [static-route property reference](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-nmcli.html).

## Windows host

The recorded state requires IPv4 forwarding on the Wi-Fi and VirtualBox host-only path, plus the persistent network route. Read-only inspection:

```powershell
Get-NetIPInterface -AddressFamily IPv4 | Select-Object InterfaceAlias, InterfaceIndex, Forwarding
Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '10.50.0.0/24'
Get-NetRoute -AddressFamily IPv4 -PolicyStore PersistentStore -DestinationPrefix '10.50.0.0/24'
```

For rebuilding the route, the equivalent administrator command is:

```text
route -p add 10.50.0.0 mask 255.255.255.0 10.60.10.1
```

Check existing entries first; forwarding must already be configured on the intended interfaces. The route command alone does not enable forwarding. Persistence semantics are described in [Microsoft's route reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/route_ws2008/). [The inspection script](../Scripts/collect-windows-lab-status.ps1) reports routes and forwarding without changing them.

## OPNsense return path

Create or inspect `KALI_RETURN_GW` on ATTACK with gateway `10.60.10.254`, then the static destination `192.168.12.172/32` using that gateway. Save/apply using the OPNsense UI so the route survives restart.

ATTACK uses the [scoped logged policy](opnsense-attack-policy.md). The internal Kali-to-DC01 path preserves source `192.168.12.172`; do not add source NAT to compensate for a missing return route.

## Verification

After any restart, inspect saved and active route values, then check Kali-to-DC01 connectivity, Nmap output, and ATTACK/LAN logging. Nmap and logs are retained in the [gallery](../Screenshots/README.md); a reboot recording is not retained. An ICMP failure by itself can reflect endpoint policy rather than a routing fault.
