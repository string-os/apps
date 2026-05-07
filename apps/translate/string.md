---
name: translate
namespace: stringhub
version: 1.0.0
description: Translate text between languages using MyMemory API. No API key required.
tags: [translate, language, multilingual, productivity]
type: app
---

# Translate

Translate text between any language pair. Powered by MyMemory (free, no API key).

**Usage:**

`/act.translate --text "Hello world" --from "en" --to "ko"`

---

## Translate Text

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

    /act.translate --text "Good morning" --from "en" --to "ko"
    /act.translate --text "오늘 날씨가 좋다" --from "ko" --to "en"
    /act.translate --text "Bonjour le monde" --from "fr" --to "ja"

---

## Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| en | English | ko | Korean |
| ja | Japanese | zh | Chinese |
| es | Spanish | fr | French |
| de | German | pt | Portuguese |
| it | Italian | ru | Russian |
| ar | Arabic | hi | Hindi |
| vi | Vietnamese | th | Thai |
| nl | Dutch | sv | Swedish |

Full list: [ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

---

## Tips

- Supports 200+ language pairs
- No API key needed (rate limit: ~5000 chars/day for anonymous)
- For heavy usage, register at mymemory.translated.net for a free API key
- Best for short texts (sentences, phrases). For documents, split into paragraphs
