# instatoon

Multi-cut Instagram comic generator with per-toon **style + tone** customization. Each comic is a *titled* series — character → N-cut storyboard (you write it) → N rendered cuts → 2×2 grids → upload-ready bundle. All outputs for one comic live in `out/<title>/`.

## v0.5 — you write the storyboard

`/act.storyboard` no longer calls Claude. The action returns a writing protocol (structure + format + rules + parameters). You write the storyboard yourself and save it to disk. Why:

- You have full context of the user's intent
- No extra API cost (~$0.05/storyboard saved)
- Direct control — easy to iterate, override, fix on the spot
- One fewer external dependency (no `ANTHROPIC_API_KEY`)

Everything else is unchanged.

## Two tuning knobs

| Knob | Affects | Default | Where applied |
|---|---|---|---|
| `--style` | Art style of the comic | `soft pastel kawaii, clean line art, light shadow` | character ref + storyboard visual-note hints + each rendered cut |
| `--tone` | Narrative voice in storyboard text | `warm conversational blog voice` | storyboard prompt (controls narration / dialogue voice) |

Both are *optional* on every action. Defaults give you a kawaii instatoon. Override for noir, minimalist, kids comic, etc.

**Consistency rule:** within one toon series, pass the **same `--style`** to character / storyboard / render. The character ref encodes the look visually; if a later cut uses a different style hint, the result drifts from the ref.

## Style preset palette

| Vibe | `--style` | `--tone` |
|---|---|---|
| **kawaii** (default) | `soft pastel kawaii, clean line art, light shadow` | `warm conversational blog voice` |
| **minimalist** | `minimalist, monochrome ink wash, lots of white space` | `quiet, observational, reflective` |
| **noir** | `noir, high-contrast black & white, dramatic shadows` | `mock-serious detective monologue` |
| **newspaper comic** | `vintage newspaper comic strip, sepia tone, halftone shading` | `dry satirical` |
| **kids** | `bright primary colors, simple bold shapes, kid-friendly` | `playful, lots of onomatopoeia` |
| **watercolor** | `soft watercolor, painterly, warm color palette` | `lyrical, prose-like` |

## Quick start

```bash
# One-time setup
string app:instatoon '/set $GEMINI_API_KEY = "AIza..."'
# (no ANTHROPIC_API_KEY needed in v0.5)
```

### Example 1 — Default kawaii style

```bash
TITLE=morning-coffee

string app:instatoon "/act.character --title $TITLE --name Luna --description 'a fluffy white cat with big eyes, wearing a tiny chef apron'"

# Storyboard: action returns guidelines. YOU write the file using the Write tool.
string app:instatoon "/act.storyboard --title $TITLE --topic 'A cat learns to make pour-over coffee and burns her paw' --cuts 12"
# (LLM reads the protocol, writes the 12-cut storyboard, saves with Write tool to
#  ~/.string/users/default/apps/instatoon/out/morning-coffee/storyboard.txt)

# Render 12 cuts (reads storyboard.txt at render time)
for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  string app:instatoon "/act.render --title $TITLE --cut $k"
done

string app:instatoon "/act.grid --title $TITLE --cuts '1,2,3,4'"
string app:instatoon "/act.grid --title $TITLE --cuts '5,6,7,8'"
string app:instatoon "/act.grid --title $TITLE --cuts '9,10,11,12'"

string app:instatoon "/act.export --title $TITLE --caption 'Luna learns pour-over ☕ #catcomic #catsofinstagram'"
```

### Example 2 — Custom noir style

```bash
TITLE=case-077
STYLE="noir, high-contrast black & white, dramatic shadows, cinematic angles"
TONE="mock-serious detective monologue"

string app:instatoon "/act.character --title $TITLE --name Detective_Rio --description '40s, trench coat, short hair, tired eyes' --style \"$STYLE\""
string app:instatoon "/act.storyboard --title $TITLE --topic 'A rookie detective revisits a 7-year cold case and finds the missing clue' --cuts 12 --tone \"$TONE\" --style \"$STYLE\""

for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  string app:instatoon "/act.render --title $TITLE --cut $k --style \"$STYLE\""
done

string app:instatoon "/act.grid --title $TITLE --cuts '1,2,3,4'"
# ... etc
string app:instatoon "/act.export --title $TITLE --caption 'Rookie detective, cold case ⚖️ #noir #coldcase'"
```

## Pipeline

```
[topic + character + title + (style + tone)]
        │
        ▼
/act.character    →  out/<title>/character.png       (--style applied)
        │
        ▼
/act.storyboard   →  out/<title>/storyboard.txt      (you write it, --tone + --style hint)
        │
        ▼  (review your storyboard before continuing!)
        │
/act.render × N   →  out/<title>/cut-1.png ... cut-N.png   (--style applied per cut)
        │
        ▼
/act.grid × ⌈N/4⌉ →  out/<title>/grid-<cuts>.png    (pure composition)
        │
        ▼
/act.export       →  out/<title>/bundle/             (everything + caption + manifest)
```

## Why `--title`?

One app can host many comic series. Each series has its own subfolder:

```
out/
├── morning-coffee/
│   ├── character.png, storyboard.txt
│   ├── cut-1.png ... cut-12.png
│   ├── grid-1,2,3,4.png ... grid-9,10,11,12.png
│   └── bundle/
└── case-077/
    ├── character.png, ...   ← different style, same app
    └── ...
```

`--title <slug>` is required on every action so files land in the right folder.

## Why these prompt rules

Three properties of recent image-gen models make instatoon automation viable:

1. **Consistency** — a character reference can be reused across cuts and stay recognizable.
2. **Emotion through action** — models render emotion better when described as physical actions ("a tear rolls down" vs "she is sad").
3. **Prop usage** — models incorporate small props/objects well, adding scene richness.

This app encodes:
- Character action mentions species / identifying trait
- Storyboard's Action field forces physical-action description, never direct emotion labels
- Render prompt explicitly distinguishes Narration (top caption), Dialogue (speech bubble), Visual note (composition only)
- Style is passed at every stage so the character ref and rendered cuts visually match

## Cost per series (12 cuts)

| Stage | Service | Approx |
|---|---|---|
| Character ref | Gemini 3 Pro Image | $0.04 |
| Storyboard | (you write it) | $0 |
| 12 cuts render | Gemini 3 Pro Image × 12 | $0.48 |
| Grid composition (3 grids) | local Python (PIL) | $0 |
| Export bundle | local bash | $0 |
| **Total** | | **~$0.52** |

For a 4-cut single-grid version: ~$0.20.

## Output structure (after a full cycle)

```
~/.string/users/default/apps/instatoon/out/<title>/
├── character.png            # Single ref image (in chosen style)
├── storyboard.txt           # N-cut script (in chosen tone)
├── cut-1.png ... cut-N.png  # rendered cuts (in chosen style)
├── grid-1,2,3,4.png
├── grid-5,6,7,8.png
├── grid-9,10,11,12.png
└── bundle/                  # Upload-ready (after /act.export)
    ├── (all of the above, copied)
    ├── caption.txt
    └── manifest.json
```

Upload to Instagram manually from `bundle/`.

## Actions

| Action | Required | Optional | Output |
|---|---|---|---|
| `/act.character` | `--title`, `--name`, `--description` | `--style`, `--filename` | `out/<title>/character.png` (Gemini API) |
| `/act.storyboard` | `--title`, `--topic` | `--cuts`, `--tone`, `--style`, `--character` | **writing protocol** → you write `out/<title>/storyboard.txt` |
| `/act.render` | `--title`, `--cut` | `--style`, `--character`, `--storyboard`, `--filename` | `out/<title>/cut-<N>.png` (Gemini API) |
| `/act.grid` | `--title`, `--cuts` (4-tuple) | — | `out/<title>/grid-<cuts>.png` (local Python) |
| `/act.export` | `--title` | `--caption` | `out/<title>/bundle/` (local bash) |

## Multi-language

Storyboard text content follows whatever language you write `--topic` and `--tone` in. A Korean topic produces Korean speech bubbles; an English topic produces English ones. The action interface, the format markers (Cut N / Narration / Dialogue / Action / Visual note), and the default tone are English; everything else is open.

## Future work (v0.6+)

- Auto-upload via Instagram Graph API (Business account)
- Hook text overlay sizing improvements for Cut 1
- Batch render (parallel API calls) for faster N-cut generation
- `/act.regenerate-cut --title T --cut K` for fixing one bad cut without redoing all
- Style preset shorthand (`--preset noir` instead of full string)
- Aspect-ratio option (1:1 default, 4:5 for feed, 9:16 for stories)
