---
name: appkit
namespace: stringhub
version: 0.1.0
description: Scaffold, validate, and learn to write SFMD apps. The meta-app for app authors.
tags: [devtools, sfmd, authoring, meta]
type: app
---

# appkit — write your own SFMD app

```
/act.new myapp                # scaffold ./myapp/ with a working starter
/act.validate ./myapp/string.md  # lint before installing
/act.examples                 # curated apps to read for patterns
```

Action signatures: `/act --help`.

## What is an SFMD app

A directory with one `string.md` file and an optional `requirements.md`.
Frontmatter declares metadata, the body is markdown the AI reads as
docs, and fenced action blocks define commands the AI can call.

`/act.new` writes a complete, working starter — open the produced
`string.md`, read the comments, edit. That's the fastest way to learn
the syntax.

## Anatomy

**Frontmatter** declares `name`, `namespace`, `version`, `type`
(`app` or `tool`). Optional: `default` (action that runs on `/open`),
`requires` (env vars surfaced as warnings if unset), `tags`,
`description`.

**Action blocks** are fenced as `act.<name>`. Six verbs: GET POST PUT
PATCH DELETE CLI. Line 1 is the verb + URI/command; remaining lines
declare fields. A field line:

    name, -n: type (required) "help text" = "default"

Types: `string`, `number`, `boolean`, `tuple`. Drop `(required)` and
add ` = "value"` for an optional field with a default. The short alias,
help text, and default are each optional.

**Response templates** (`act.<name>.response`) shape what the AI sees
back. Reference fields with `{Response.body.X}`, iterate arrays with
`for: x in Response.body.items ... end:`. Declare value shortcuts with
`{@var} = expr` so the AI calls back with `@var-3` instead of typing
long IDs. Tuple form: `{@card} = ({number}, {repo})`, indexed in
later templates as `{card[0]}`, `{card[1]}`.

**Sibling files** — any non-`.md` file in the app directory ships
alongside `string.md`, with executable mode preserved. Use this for
shell helpers when an action needs multiple steps.

## Iterate

```
appkit new myapp                     # writes ./myapp/string.md
appkit validate ./myapp/string.md    # lint
string /install --app ./myapp        # install locally
string app:myapp                     # try it
```

After every edit to `string.md`, reinstall to pick up changes.
`/act.validate` catches the common mistakes (missing frontmatter
fields, malformed action blocks, dangling sibling-script refs)
before install.

## When stuck

Run `/act.examples` for a curated list of apps to read. Each one is
short and demonstrates a specific pattern: simple GET, auth header,
multi-step CLI, tuple shortcuts, or full feed/comment chain.

[!requirements](./requirements.md)

```act.new
CLI ./appkit new {name} {type} {dir}
  name, -n: string (required) "App name (alphanumeric + hyphens)"
  type, -t: string "app | tool" = "app"
  dir, -d:  string "Parent directory" = "."
```

```act.new.response
{Response.body}
```

```act.validate
CLI ./appkit validate {path}
  path, -p: string (required) "Path to string.md"
```

```act.validate.response
{Response.body}
```

```act.examples
CLI ./appkit examples
```

```act.examples.response
{Response.body}
```
