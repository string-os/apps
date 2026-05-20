---
name: humanizer
namespace: stringhub
version: 1.0.1
description: Detect and fix signs of AI-generated writing. Make text sound natural and human-written.
tags: [productivity, writing, editing, ai-detection, humanize, text, proofreading]
type: app
default: check
---

[!requirements](./requirements.md)

# Humanizer

Detect common signs of AI-generated writing — overused vocabulary (`delve`, `crucial`, `leverage`, `utilize`, …), em dash overuse, rule-of-three lists (`X, Y, and Z`), negative parallelism (`not only … but also …`), vague attributions (`it is worth noting`). Runs locally with regex, no API.

## Actions

- `/act.check --text <string>` — scan text and list detected AI patterns

```act.check
CLI python3 -c "import re,sys;t=sys.argv[1].lower();ws=[w for w in ['delve','crucial','robust','comprehensive','nuanced','leverage','utilize','streamline','foster','facilitate','moreover','furthermore','additionally','landscape','paradigm','multifaceted','pivotal','embark','realm','testament','tapestry','underscores'] if w in t];ps=[];em=len(re.findall(r' — ',t));ro3=len(re.findall(r'\w+, \w+, and \w+',t));neg='not only' in t and 'but also' in t;vag=bool(re.search(r'it is (important|worth)',t));[ps.append('Em dash overuse') for _ in range(1) if em>0];[ps.append('Rule of three') for _ in range(1) if ro3>0];[ps.append('Negative parallelism') for _ in range(1) if neg];[ps.append('Vague attribution') for _ in range(1) if vag];n=len(ws)+len(ps);print('## AI Pattern Check');print();[print('- **AI word:** ' + chr(96) + w + chr(96)) for w in ws];[print('- **Pattern:** ' + p) for p in ps];print();print('**Found ' + str(n) + ' pattern(s).**' if n>0 else 'No AI patterns detected.')" "{text}"
  text: string (required) "Text to analyze"
```
