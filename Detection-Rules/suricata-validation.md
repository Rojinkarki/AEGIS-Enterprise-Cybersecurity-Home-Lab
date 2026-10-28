# Suricata IDS validation

## Recorded state

Suricata is deployed inside OPNsense in IDS / alert-only mode with ET Open rules. The completed build records a prior alert for SID `2100498`, `GPL ATTACK_RESPONSE id check returned root`.

The latest source conversation reported no matching alert during recapture and moved on to Nmap/firewall evidence. Its terminal image showed repeated test requests without the expected response body. No fresh Suricata success or alert screenshot is included in this release. The text `uid=0(root)` in this test is an IDS test pattern, not evidence that the lab obtained root access.

## Repeat the controlled test

1. In OPNsense, inspect Services > Intrusion Detection > Administration. Confirm IDS is running, the relevant ET Open rule is installed/enabled, and the monitored interface actually sees WS01's traffic.
2. From WS01, make the documented test request:

   ```powershell
   curl.exe http://testmyids.org/uid/index.html
   ```

3. Confirm that the HTTP response contains `uid=0(root)`. A blank response, redirect or blocked request does not establish that the signature's payload traversed the sensor.
4. In the OPNsense IDS alert view, select the relevant time range and look for SID 2100498 and the matching signature. Retain timestamp, source/destination, interface and action.
5. If absent, inspect response, capture path, rule state, home-network settings and time filters before drawing a conclusion. Record the unsuccessful result if it remains absent.

The external endpoint can change or be unavailable. This procedure is an example from the [official Suricata quickstart](https://docs.suricata.io/en/latest/quickstart.html), not an automated release test. [OPNsense IDS documentation](https://docs.opnsense.org/manual/ips.html) explains interface selection and the loss of endpoint attribution when capturing after NAT. Same-subnet VM traffic does not necessarily cross this sensor.
