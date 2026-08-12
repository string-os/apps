---
title: Senior Security
name: senior-security
namespace: stringhub
type: app
version: 0.1.0
description: "Comprehensive security engineering skill for application security, penetration testing, security architecture, and compliance auditing. Includes security assessment tools, threat modeling, crypto implementation, and security automation. Use when designing security architecture, conducting penetration tests, implementing cryptography, or performing security audits."
tags: [security, pentest, threat-modeling, audit, cryptography]
---

# Senior Security

Security-engineering helpers. Each action runs a bundled analyzer over a target path and
prints a findings report — call the action instead of writing the analysis yourself. The
three actions differ by lens: `threat_modeler` enumerates assets/entry points and models
threats; `security_auditor` flags code/config security issues with remediation; `pentest_automator`
runs automated penetration-test checks against the target.

**All three share one interface:** a required `target` String field, plus an `extra_args`
field carrying the optional flags as ONE space-separated string. Optional flags (all):
`[--verbose | -v]` (detailed output) `[--json]` (machine-readable findings) `[--output <file> | -o <file>]`
(write report to a file instead of stdout). Defaults: human-readable report to stdout.
**Passthrough gotcha:** an `extra_args` value cannot begin with `--`; the flags above don't take
such values, so just pass e.g. `--json -o report.txt`.

## Analyze a target
- **`/act.threat_modeler`** `--target <path>` `[--verbose]` `[--json]` `[--output <file>]` — threat-model
  a project path: enumerate assets/entry points and surface findings.
- **`/act.security_auditor`** `--target <path>` `[--verbose]` `[--json]` `[--output <file>]` — audit a
  path for security issues and emit recommendations.
- **`/act.pentest_automator`** `--target <path>` `[--verbose]` `[--json]` `[--output <file>]` — run
  automated penetration-test checks against a target/scope.

Deep-reference docs are bundled under `references/` (security architecture patterns,
penetration-testing guide, cryptography implementation) — the flags above are complete, so
you shouldn't need them.

```act.threat_modeler
CLI ./scripts/_argshim.sh ./scripts/threat_modeler.py "{target}" "{extra_args}"
  target: string (required) "Project path to analyze for threat modeling"
  extra_args: string (optional) "Additional flags, e.g. --verbose --json -o out.txt" = ""
```

```act.security_auditor
CLI ./scripts/_argshim.sh ./scripts/security_auditor.py "{target}" "{extra_args}"
  target: string (required) "Target path to audit for security issues"
  extra_args: string (optional) "Additional flags, e.g. --verbose --json -o out.txt" = ""
```

```act.pentest_automator
CLI ./scripts/_argshim.sh ./scripts/pentest_automator.py "{target}" "{extra_args}"
  target: string (required) "Target path or scope for the penetration test"
  extra_args: string (optional) "Additional flags, e.g. --verbose --json -o out.txt" = ""
```
