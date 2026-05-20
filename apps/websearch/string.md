---
name: websearch
namespace: stringhub
version: 1.0.2
description: Web search across multiple engines. DuckDuckGo, Wikipedia, and Hacker News. No API key required.
tags: [search, web, duckduckgo, wikipedia, hacker-news, research]
type: app
---

[!requirements](./requirements.md)

# Web Search

Search the web from String. DuckDuckGo for general queries, Wikipedia for encyclopedia entries, Hacker News for tech news. No API key.

## Actions

- `/act.search --query <text>` — DuckDuckGo instant answer (best for factual queries)
- `/act.wiki --query <article-title>` — Wikipedia article summary (use exact capitalized title)
- `/act.hn` — Hacker News front page (top 10)
- `/act.hn_search --query <text> [--hitsPerPage 10]` — Hacker News search

```act.search
GET https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1
  query: string (required) "Search query"
```

```act.search.response
## {Response.body.Heading}

{Response.body.AbstractText}

**Source:** {Response.body.AbstractURL}
```

```act.wiki
GET https://en.wikipedia.org/api/rest_v1/page/summary/{query}
  query: string (required) "Article title (e.g. Markdown, Python, Seoul)"
```

```act.wiki.response
## {Response.body.title}

{Response.body.extract}

**Read more:** {Response.body.content_urls.desktop.page}
```

```act.hn
GET https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10
```

```act.hn.response
## Hacker News — Front Page

for: hit in Response.body.hits
- **{hit.title}** ({hit.points} pts, {hit.num_comments} comments) — https://news.ycombinator.com/item?id={hit.objectID}
end:
```

```act.hn_search
GET https://hn.algolia.com/api/v1/search?tags=story
  query: string (required) "Search query"
  hitsPerPage: number (optional) "Max results" = "10"
```

```act.hn_search.response
## Hacker News — Results

for: hit in Response.body.hits
- **{hit.title}** ({hit.points} pts, {hit.num_comments} comments) — https://news.ycombinator.com/item?id={hit.objectID}
end:
```
