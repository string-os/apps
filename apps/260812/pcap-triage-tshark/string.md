---
title: Pcap Triage Tshark
name: pcap-triage-tshark
namespace: stringhub
type: app
version: 0.2.0
description: "Fast workflow to inspect PCAPs and extract protocol-level details using tshark"
tags: [network, pcap, tshark, triage]
---

# PCAP Triage with tshark

Triage a PCAP's HTTP traffic without writing tshark commands — the action runs tshark
under the hood and returns a parseable summary.

The one flag is listed inline below (required). The action prints the summary; you should
not need `/act.summarize_http_requests --help`.

## Triage
- **`/act.summarize_http_requests`** `--pcap <path>` — per-request table (time, src ip:port,
  method, uri) plus a best-effort count of requests carrying the `X-TLM-Mode: exfil` header.
  Use this first to see the HTTP shape of a capture and spot exfil-flavored requests.

## What to triage in HTTP requests
- Start broad, then narrow to the one flow/stream that matters.
- Confirm where the signal lives: request URI/query vs. a header vs. the body. The same
  string can appear in any of them and that changes how you'd match it.
- Note which parts are invariant vs. variable across requests — that's what a detection
  rule keys on.

```act.summarize_http_requests
CLI bash ./scripts/summarize_http_requests.sh "{pcap}"
  pcap: string (required) "Path to the PCAP file to summarize"
```
