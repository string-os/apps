---
name: humanizer
namespace: stringhub
version: 1.0.0
description: Detect and fix signs of AI-generated writing. Make text sound natural and human-written.
tags: [productivity, writing, editing, ai-detection, humanize, text, proofreading]
type: app
default: check
---

# Humanizer

Detect and fix common signs of AI-generated writing. Based on known AI writing patterns.

`/act.check --text "This is a text to check"`

---

## Check Text for AI Patterns

```act.check
CLI python3 -c "import re,sys;t=sys.argv[1].lower();ws=[w for w in ['delve','crucial','robust','comprehensive','nuanced','leverage','utilize','streamline','foster','facilitate','moreover','furthermore','additionally','landscape','paradigm','multifaceted','pivotal','embark','realm','testament','tapestry','underscores'] if w in t];ps=[];em=len(re.findall(r' — ',t));ro3=len(re.findall(r'\w+, \w+, and \w+',t));neg='not only' in t and 'but also' in t;vag=bool(re.search(r'it is (important|worth)',t));[ps.append('Em dash overuse') for _ in range(1) if em>0];[ps.append('Rule of three') for _ in range(1) if ro3>0];[ps.append('Negative parallelism') for _ in range(1) if neg];[ps.append('Vague attribution') for _ in range(1) if vag];n=len(ws)+len(ps);print('## AI Pattern Check');print();[print('- **AI word:** ' + chr(96) + w + chr(96)) for w in ws];[print('- **Pattern:** ' + p) for p in ps];print();print('**Found ' + str(n) + ' pattern(s).**' if n>0 else 'No AI patterns detected.')" "{text}"
  text: string (required) "Text to analyze"
```

---

## Common AI Writing Patterns

### Words to Avoid
`delve`, `crucial`, `robust`, `comprehensive`, `nuanced`, `leverage`, `utilize`, `streamline`, `foster`, `facilitate`, `moreover`, `furthermore`, `pivotal`, `embark`, `realm`, `testament`, `tapestry`, `multifaceted`

### Structural Patterns
- **Em dash overuse** — AI loves em dashes (—) where commas or periods work better
- **Rule of three** — "X, Y, and Z" repeated throughout
- **Negative parallelism** — "not only X but also Y"
- **Vague attributions** — "It is worth noting that..."
- **Cliche openings** — "In today's digital landscape..."

### Quick Fixes
1. Replace AI vocabulary with plain words: `utilize` → `use`, `leverage` → `use`, `facilitate` → `help`
2. Break em dashes into separate sentences
3. Vary sentence structure — not every list needs three items
4. Be specific instead of vague: "Experts say" → name the expert or cut it
5. Start paragraphs differently — avoid "Moreover," "Furthermore," "Additionally,"
