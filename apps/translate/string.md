---
name: translate
namespace: stringhub
version: 1.0.1
description: Translate text between languages using MyMemory API. No API key required.
tags: [translate, language, multilingual, productivity]
type: app
---

[!requirements](./requirements.md)

# Translate

Translate text between any language pair. Powered by [MyMemory](https://mymemory.translated.net) (free, no API key).

## Actions

- `/act.translate --text <string> --from <code> --to <code>` — translate between two ISO 639-1 codes (e.g. `en`, `ko`, `ja`, `zh`, `es`, `fr`, `de`)

```act.translate
GET https://api.mymemory.translated.net/get?q={text}&langpair={from}|{to}
  text: string (required) "Text to translate"
  from: string (required) "Source language code (e.g. en, ko, ja, zh, es, fr, de)"
  to: string (required) "Target language code"
```

```act.translate.response
## Translation

> {Response.body.responseData.translatedText}

- **Match quality:** {Response.body.responseData.match}
- **Status:** {Response.body.responseStatus}
```
