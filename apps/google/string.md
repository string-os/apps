---
name: google
namespace: stringhub
version: 1.0.1
description: Google Workspace client. Gmail, Calendar, and Drive via gcloud ADC + REST APIs.
tags: [google, gmail, calendar, drive, workspace, productivity]
type: app
---

[!requirements](./requirements.md)

[!nav:main](./nav/main.md)

# Google Workspace

Gmail, Calendar, and Drive — all from String. Authentication uses `gcloud` Application Default Credentials (one-time human-driven OAuth) — see `requirements.md`. No env var to set; each action fetches a fresh access token via `gcloud auth print-access-token`.

## Pages

- `@main.gmail` — read, search, send email
- `@main.calendar` — agenda, create / search / delete events
- `@main.drive` — list, search, download files
