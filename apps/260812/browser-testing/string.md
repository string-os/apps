---
title: Browser Testing
name: browser-testing
namespace: stringhub
type: app
version: 0.2.0
description: "VERIFY your changes work. Measure CLS, detect theme flicker, test visual stability, check performance. Use BEFORE and AFTER making changes to confirm fixes. Includes ready-to-run scripts: measure-cls.ts, detect-flicker.ts"
tags: [browser, performance, cls, playwright, visual-stability]
---

# Browser Testing

Verify front-end fixes by measuring a running page with Playwright/CDP. Run an action
BEFORE and AFTER a change to confirm it actually helped — the daemon drives the browser,
so you just point an action at a URL (page or API endpoint) and read the JSON it returns.

Every action's flags are listed inline below (required unless shown in `[...]`, which
marks an optional flag with its default). Each action prints JSON; you should not need
`/act.<name> --help`.

## Measure
- **`/act.measure`** `--url <url>` — load times + network waterfall + Chrome perf counters for a page or API endpoint. Use to find slow/sequential requests, high `LayoutCount`, or heavy `ScriptDuration`. Sequential request waterfalls usually mean serial `await`s that should be `Promise.all()`.
- **`/act.measure_cls`** `--url <url>` `[--scroll]` (default off) — Cumulative Layout Shift (CLS) score + rating. CLS < 0.1 is good, 0.1–0.25 needs improvement, > 0.25 is poor. `--scroll` carries the literal sub-flag (pass `--scroll "--scroll"`) to scroll the page and catch shifts from below-the-fold / late-loading content.
- **`/act.detect_flicker`** `--url <url>` — detect dark-theme flash-of-white: sets the theme in localStorage, then checks the background color at first paint.

## Interpreting results
CLS only counts shifts inside the viewport, so measure with `--scroll` (and ideally after
triggering a UI action like a theme toggle) for late content. Absolute numbers vary run to
run (build, viewport, timing) — the before/after *relative* change is what matters.

```act.measure
CLI npx ts-node ./measure.ts "{url}"
  url: string (required) "URL to measure, e.g. http://localhost:3000"
```

```act.measure_cls
CLI npx ts-node ./measure-cls.ts "{url}" {scroll}
  url: string (required) "URL to measure CLS for, e.g. http://localhost:3000"
  scroll: string (optional) "Pass --scroll to scroll the page and catch more shifts" = ""
```

```act.detect_flicker
CLI npx ts-node ./detect-flicker.ts "{url}"
  url: string (required) "URL to check for theme flicker, e.g. http://localhost:3000"
```
