# Read-only inspection on the Windows virtualization host.
$ErrorActionPreference = 'Stop'

$aegisAddresses = @('192.168.12.180', '10.60.10.254')
$aegisInterfaces = @(Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -in $aegisAddresses })
if ($aegisInterfaces.Count -eq 0) {
    throw 'The recorded AEGIS host addresses were not found. Check this host and its addressing.'
}

Write-Output 'AEGIS host addresses'
$aegisInterfaces | Select-Object InterfaceAlias, InterfaceIndex, IPAddress, PrefixLength

Write-Output 'IPv4 forwarding on the recorded host interfaces'
Get-NetIPInterface -AddressFamily IPv4 |
    Where-Object { $_.InterfaceIndex -in $aegisInterfaces.InterfaceIndex } |
    Select-Object InterfaceAlias, InterfaceIndex, Forwarding

foreach ($aegisStore in @('ActiveStore', 'PersistentStore')) {
    Write-Output "AEGIS route in $aegisStore"
    $aegisRoutes = @(Get-NetRoute -AddressFamily IPv4 -PolicyStore $aegisStore |
        Where-Object { $_.DestinationPrefix -eq '10.50.0.0/24' })
    if ($aegisRoutes.Count -eq 0) {
        Write-Warning "No AEGIS network route found in $aegisStore."
    }
    $aegisRoutes | Select-Object DestinationPrefix, NextHop, InterfaceIndex, RouteMetric
}
