---
name: websearch
namespace: stringhub
version: 1.0.0
description: Web search across multiple engines. DuckDuckGo, Wikipedia, and Hacker News. No API key required.
tags: [search, web, duckduckgo, wikipedia, hacker-news, research]
type: app
---

# Web Search

Search the web from String. DuckDuckGo for general search, Wikipedia for knowledge, Hacker News for tech trends. No API key needed.

---

## Web Search (DuckDuckGo)

`/act.search --query "string flavored markdown"`

```act.search
GET https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1
  query: string (required) "Search query"
```

```act.search.response
## {Response.body.Heading}

{Response.body.AbstractText}

**Source:** {Response.body.AbstractURL}
```

---

## Wikipedia

`/act.wiki --query "Markdown"`

```act.wiki
GET https://en.wikipedia.org/api/rest_v1/page/summary/{query}
  query: string (required) "Article title (e.g. Markdown, Python, Seoul)"
```

```act.wiki.response
## {Response.body.title}

{Response.body.extract}

**Read more:** {Response.body.content_urls.desktop.page}
```

---

## Hacker News — Top Stories

`/act.hn`

```act.hn
GET https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=10
```

```act.hn.response
## Hacker News — Front Page

{Response.body.nbHits} stories on front page.
```

---

## Hacker News — Search

`/act.hn_search --query "AI agents"`

```act.hn_search
GET https://hn.algolia.com/api/v1/search?tags=story
  query: string (required) "Search query"
  hitsPerPage: number (optional) "Max results" = "10"
```

```act.hn_search.response
## Hacker News Results

{Response.body.nbHits} results found.
```

---

## Tips

- DuckDuckGo instant answers work best for factual queries
- Wikipedia search uses exact article titles — try capitalized proper names
- Hacker News top stories refresh every few minutes
- All APIs are free with no rate limits for normal usage
- Requires: `curl`, `python3` (pre-installed on most systems)
