# AEGIS Incident Report IR-001

## Incident Title
Multiple Failed Active Directory Login Attempts

## Severity
High

## Detection Source
Splunk Enterprise

## Detection Rule
AEGIS - Multiple Failed Login Attempts

## Date
August 27, 2026

## Affected Systems
- DC01 - 10.50.0.10
- WS01 - 10.50.0.30

## Target Account
CORP\acarter

## Detection Logic
The Splunk alert detects 5 or more Windows failed logon events
(Event ID 4625) on the same host within a 15-minute period.

## Relevant Windows Event
Event ID: 4625

Description:
An account failed to log on.

## Observed Activity
Multiple failed authentication attempts were generated from WS01
against the CORP\acarter account while attempting to access a
network resource on DC01.

The failed attempts generated Windows Security Event ID 4625
events on the domain controller.

## Authentication Type
Logon Type 3 - Network Logon

## Detection Flow

WS01
  v
Failed authentication attempts
  v
DC01 Windows Security Log
  v
Event ID 4625
  v
Splunk Universal Forwarder
  v
SOC01 Splunk Enterprise
  v
AEGIS Detection Rule
  v
Alert Triggered

## Investigation

The alert was investigated in Splunk using Windows Security
Event ID 4625.

Important fields reviewed included:

- Account Name
- Account Domain
- Logon Type
- Workstation Name
- Source Network Address
- Failure Reason
- Status
- Sub Status

The activity was identified as a controlled AEGIS lab simulation.

## Classification
True Positive - Authorized Security Test

## Impact
No production impact.

No account compromise occurred.

The activity was intentionally generated as part of the
AEGIS detection engineering lab.

## Response
The authentication attempts were reviewed and correlated
with the originating workstation.

No containment action was required because the activity
was authorized.

## Lessons Learned
- Windows Event ID 4625 provides detailed failed authentication telemetry.
- Splunk can aggregate repeated authentication failures into actionable detections.
- A single failed password attempt should not necessarily generate an incident.
- Threshold-based detection helps distinguish normal user mistakes from suspicious activity.
- Investigation context is required before determining whether an alert represents malicious behavior.

## Status
Closed - Authorized Simulation
