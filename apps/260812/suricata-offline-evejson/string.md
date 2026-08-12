---
title: Suricata Offline Evejson
name: suricata-offline-evejson
namespace: stringhub
type: app
version: 0.2.0
description: "Running Suricata against PCAPs offline and validating results via eve.json"
tags: [network, suricata, ids, eve-json]
---

# Suricata Offline Mode + EVE JSON

Replay a PCAP through Suricata offline and read back the alerts — the action runs Suricata
into a fresh log dir, parses `eve.json`, and returns a `signature_id -> count` table.

All flags are listed inline below (required unless shown in `[...]`, which marks an
optional flag with its default). The action prints a `signature_id -> count` table; you
should not need `/act.run_suricata_offline --help`.

## Run + check
- **`/act.run_suricata_offline`** `--pcap <path>` `[--rules <file>]` (default `/root/local.rules`)
  `[--log_dir <dir>]` (default `/tmp/suri`) — run Suricata on one PCAP with a rules file,
  then summarize the alerts fired. Use it to confirm whether a rule fires (and how many
  times) on a given capture.

## Reading the results
- An alert count of `0` means no rule matched that traffic — expected for known-negative
  PCAPs, a problem for known-positive ones.
- Validate a rule by running it against BOTH positive and negative captures: it should
  alert on the positive and stay silent on the negative. A rule that fires on both is too
  broad; one that fires on neither doesn't match at all.
- Each run uses a fresh log dir so old alerts don't bleed into the new summary.

```act.run_suricata_offline
CLI bash ./scripts/run_suricata_offline.sh "{pcap}" "{rules}" "{log_dir}"
  pcap: string (required) "Path to the PCAP to replay through Suricata"
  rules: string (optional) "Rules file (default /root/local.rules)" = "/root/local.rules"
  log_dir: string (optional) "Log directory for eve.json (default /tmp/suri)" = "/tmp/suri"
```
