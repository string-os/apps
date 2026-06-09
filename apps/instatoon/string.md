---
name: instatoon
namespace: stringhub
version: 0.5.0
description: Topic → multi-cut Instagram comic. Per-toon style+tone, multiple series per app, the agent writes the storyboard itself, Gemini renders the cuts.
tags: [creator, instatoon, comic, instagram, gemini]
type: app
requires: [GEMINI_API_KEY]
default: character
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# instatoon

Make many comic series in one app. Each comic is identified by a `--title` slug and
lives in its own `out/<title>/` subfolder. Visual `--style` and narrative `--tone` are
tunable per toon (defaults give a soft pastel kawaii look + warm conversational voice).

```
/act.character  --title T → out/T/character.png  (--style applied)
/act.storyboard --title T → out/T/storyboard.txt (--tone + --style applied)
/act.render     --title T --cut K → out/T/cut-K.png (--style applied)
/act.grid       --title T --cuts "1,2,3,4" → out/T/grid-*.png (composition only)
/act.export     --title T → out/T/bundle/
```

`--title` is **required** on every action. `--style` and `--tone` are optional — leave
them off for the kawaii default.

## Two knobs

| Knob | Applied at | Default |
|---|---|---|
| `--style` | character ref, render of each cut, storyboard's visual-note hints | `soft pastel kawaii, clean line art, light shadow` |
| `--tone` | storyboard text only (narration / dialogue / action voice) | `warm conversational blog voice` |

**Consistency rule:** within one toon series, pass the **same `--style`** to
`/act.character`, `/act.storyboard`, and every `/act.render`. The character ref
encodes the look visually; a later cut with a different style hint will drift.

## Style presets

| Vibe | `--style` | `--tone` |
|---|---|---|
| kawaii (default) | `soft pastel kawaii, clean line art, light shadow` | `warm conversational blog voice` |
| minimalist | `minimalist, monochrome ink wash, lots of white space` | `quiet, observational, reflective` |
| noir | `noir, high-contrast black & white, dramatic shadows` | `mock-serious detective monologue` |
| newspaper comic | `vintage newspaper comic strip, sepia tone, halftone shading` | `dry satirical` |
| kids | `bright primary colors, simple bold shapes, kid-friendly` | `playful, lots of onomatopoeia` |
| watercolor | `soft watercolor, painterly, warm color palette` | `lyrical, prose-like` |

## Cut convention

```
Cut 1            : Thumbnail — the hook (large text, strong emotion)
Cut 2..N-1       : Body — beginning → conflict → climax → resolution
Cut N            : CTA — ask for like/follow/share
```

## Workflow

1. `/act.character --title T --name X --description "..." [--style "..."]` — once
2. `/act.storyboard --title T --topic "..." --cuts 12 [--tone "..."] [--style "..."]` —
   once. **The action returns a writing protocol; you write the storyboard yourself
   and save it to the path the response gives you.**
3. `/act.render --title T --cut K [--style "..."]` — N times (run sequentially)
4. `/act.grid --title T --cuts "1,2,3,4"` — ⌈N/4⌉ times
5. `/act.export --title T --caption "..."` — once

## Examples

**Default (kawaii):**
```
TITLE=morning-coffee
string app:instatoon "/act.character --title $TITLE --name Luna --description 'a fluffy white cat with big eyes, wearing a tiny chef apron'"
string app:instatoon "/act.storyboard --title $TITLE --topic 'A cat learns to make pour-over coffee and burns her paw' --cuts 12"
# ... agent writes storyboard.txt ...
for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  string app:instatoon "/act.render --title $TITLE --cut $k"
done
string app:instatoon "/act.grid --title $TITLE --cuts '1,2,3,4'"
# ... grids 5,6,7,8 and 9,10,11,12 ...
string app:instatoon "/act.export --title $TITLE --caption 'Luna learns pour-over ☕ #catcomic #catsofinstagram'"
```

**Noir style override:**
```
TITLE=case-077
STYLE="noir, high-contrast black & white, dramatic shadows"
TONE="mock-serious detective monologue"
string app:instatoon "/act.character --title $TITLE --name Detective_Rio --description '40s, trench coat, tired eyes, short hair' --style \"$STYLE\""
string app:instatoon "/act.storyboard --title $TITLE --topic 'A rookie detective revisits a 7-year cold case and finds the missing clue' --cuts 12 --tone \"$TONE\" --style \"$STYLE\""
for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  string app:instatoon "/act.render --title $TITLE --cut $k --style \"$STYLE\""
done
```

## Prompt tips

When writing character descriptions:
1. **Mention species / identifying trait** — e.g. "a snowman character", "a golden retriever puppy"
2. **Express emotion through action**, never through labels — "tears roll down her cheek", not "she is sad"

These two rules alone make output dramatically more consistent and expressive.

## Multi-language

Storyboard text content follows whatever language you write the `--topic` and `--tone`
in. Korean topics produce Korean speech bubbles; English topics produce English ones.
The action interface, the format markers, and the default tone are English; everything
else is open.

---

```act.character
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Character reference sheet for an instatoon, white background, single character: {description}. Character name: {name}. Visual style: {style}. Show the character in a neutral pose, expressing emotion through body language. High consistency, recognizable silhouette."}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":{"imageSize":"1K","aspectRatio":"1:1"}}}'
  title, -T: string (required) "Toon slug (folder name)"
  name, -n: string (required) "Character name"
  description, -d: string (required) "Visual description (mention species/identifying traits)"
  style, -y: string "Art style — keep it consistent across storyboard/render" = "soft pastel kawaii, clean line art, light shadow"
  filename, -f: string "Output PNG path" = "$HOME/apps/instatoon/out/{title}/character.png"
```

```act.character.response
save: candidates[0].content.parts[0].inlineData.data
decode: base64
to: {filename}
{character_name} = {name}
{character_description} = {description}
Character "{name}" for toon "{title}" saved → {filename}
  style applied: {style}

next: /act.storyboard --title {title} --topic "..." --cuts 12 --style "{style}"
```

---

```act.storyboard
CLI echo "storyboard protocol delivered for {title}"
  title, -T: string (required) "Toon slug"
  topic, -t: string (required) "What the comic is about"
  cuts: number "Total cut count" = "12"
  character, -c: string "Character name + short description" = "{character_name} ({character_description})"
  tone, -o: string "Narrative voice for the storyboard text" = "warm conversational blog voice"
  style, -y: string "Visual style hint (used in visual-note generation)" = "soft pastel kawaii, clean line art, light shadow"
```

```act.storyboard.response
# 📋 Storyboard writing protocol — {title}

**You (the calling LLM) write the storyboard yourself, then save it to:**
`~/.string/users/default/apps/instatoon/out/{title}/storyboard.txt`

## Parameters

- **Topic:** {topic}
- **Cuts:** {cuts}
- **Character:** {character}
- **Tone:** {tone}
- **Visual style hint:** {style}

## Structure (must follow)

- Cut 1: thumbnail. Hook line. Big emotion, strong expression.
- Cut 2 ~ {cuts}-1: body (setup → tension → climax → resolution)
- Cut {cuts}: CTA (ask for like / follow / share)

## Output format (required — every cut must use this exact shape)

```
## Cut N
- Narration: <caption text rendered at top of the panel. 1 sentence, tone-matched.>
- Dialogue: <what the character says inside a speech bubble. 1-2 sentences, tone-matched. "none" if there is no dialogue.>
- Action: <emotion expressed as a physical action. 1 sentence. e.g. "a tear rolls down her cheek">
- Visual note: <background / props / composition. Render uses this to draw the scene only. 1 sentence.>
```

## Rules

- Every cut features the same character. Stay consistent.
- Never describe emotion directly. Always express it through action.
- Language: write narration/dialogue/action in whatever language fits {tone} and {topic}.
- Output cuts 1 through {cuts} only. No headers, no extra commentary.
- Apply {tone} consistently to narration and dialogue voice.

## What you do next

1. Write the storyboard text following structure + format + rules above.
2. Save with the Write tool to:
   `~/.string/users/default/apps/instatoon/out/{title}/storyboard.txt`
3. (Optional) Self-review: are the cuts well-distributed? Is the tone consistent?
   Do visual notes match the {style}?

## Why you write it (not an API call)

- You have full context from the user's intent and prior decisions
- No extra API cost (~$0.05/storyboard saved)
- No API latency — instant
- Direct control: easy to iterate or override mid-stream

next: /act.render --title {title} --cut 1 --style "{style}", ... --cut {cuts}
```

---

```act.render
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"inlineData":{"mimeType":"image/png","data":"{character|base64file}"}},{"text":"You are illustrating an instatoon (Instagram comic). Render ONLY cut #{cut}. Match the character in the reference image exactly: same colors, proportions, hairstyle, glasses, facial hair, clothing.\n\n# Visual style (use throughout)\n{style}\n\n# Text rendering rules (CRITICAL)\n- Narration → render as a clean caption banner at the TOP of the panel, in the same language as the storyboard.\n- Dialogue → render the EXACT text from the storyboard inside a comic-style speech bubble next to the character. If Dialogue is \"none\", do NOT draw a speech bubble.\n- Visual note → informs composition, background, props. Never draw this text — only the scene it describes.\n- Emotion: show it through facial expression + body language + props. Never draw labels like \"sad\" or \"happy\".\n- Cut 1 (thumbnail): add a LARGE hook text overlay (the Narration line, oversized).\n- Last cut (CTA): include a subtle like/follow visual hint per Visual note.\n\n# Format\n1:1 square, white or light textured background (unless the style dictates otherwise).\n\n# Storyboard (use ONLY the section for cut #{cut})"},{"text":"{storyboard|file}"}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":{"imageSize":"1K","aspectRatio":"1:1"}}}'
  title, -T: string (required) "Toon slug"
  cut, -c: number (required) "Cut number"
  style, -y: string "Visual style — MUST match the character ref's style" = "soft pastel kawaii, clean line art, light shadow"
  character: string "Character ref PNG" = "$HOME/apps/instatoon/out/{title}/character.png"
  storyboard: string "Storyboard text path (read at render time)" = "$HOME/apps/instatoon/out/{title}/storyboard.txt"
  filename, -f: string "Output PNG path" = "$HOME/apps/instatoon/out/{title}/cut-{cut}.png"
```

```act.render.response
save: candidates[0].content.parts[0].inlineData.data
decode: base64
to: {filename}
Cut {cut} of "{title}" rendered → {filename}
  style: {style}

next: /act.render --title {title} --cut <next>  ·  after the final cut: /act.grid --title {title} --cuts "1,2,3,4"
```

---

```act.grid
CLI bash $HOME/packages/instatoon/grid.sh $HOME/apps/instatoon/out/{title} {cuts}
  title, -T: string (required) "Toon slug"
  cuts, -c: string (required) "Comma-separated 4 cut numbers, e.g. 1,2,3,4"
```

```act.grid.response
{Response.body}

next: /act.grid --title {title} --cuts <next four>  ·  /act.export --title {title}
```

---

```act.export
CLI bash $HOME/packages/instatoon/export.sh $HOME/apps/instatoon/out/{title} {caption}
  title, -T: string (required) "Toon slug"
  caption, -c: string "Instagram caption" = ""
```

```act.export.response
{Response.body}

next: upload the bundle manually  ·  /act.character --title <new-toon> for the next series
```
