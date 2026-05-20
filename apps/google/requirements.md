# Requirements

> **AI agents:** This app needs a one-time **human-driven OAuth login** before any action will work. You cannot complete it yourself — it opens a browser for the human to confirm Google account permissions. Ask the human to run step 2 below and confirm "done" before retrying actions.

## 1. Install gcloud

If `which gcloud` returns nothing, follow [the install guide](https://cloud.google.com/sdk/docs/install).

## 2. Human runs OAuth login with Workspace scopes

```bash
gcloud auth login --update-adc \
  --scopes=openid,\
https://www.googleapis.com/auth/userinfo.email,\
https://www.googleapis.com/auth/gmail.modify,\
https://www.googleapis.com/auth/drive,\
https://www.googleapis.com/auth/calendar
```

A browser opens; the human signs in and approves Gmail / Drive / Calendar access. Credentials are stored in Application Default Credentials (`~/.config/gcloud/application_default_credentials.json`) and auto-refresh.

## 3. Verify

```bash
gcloud auth print-access-token   # should print an ya29... token
gcloud config get-value account  # should print the email used
```

To switch accounts, the human re-runs `gcloud auth login --update-adc ...` with a different account. To revoke: <https://myaccount.google.com/permissions>.
