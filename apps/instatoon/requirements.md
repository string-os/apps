# Requirements

## Environment Variables

| Variable | Required | Description | How to obtain |
|----------|----------|-------------|---------------|
| `$GEMINI_API_KEY` | Yes | Used by `/act.character` and `/act.render` for image generation (Gemini 3 Pro Image / Nano Banana Pro) | https://aistudio.google.com/apikey |

Setup:
```
string app:instatoon '/set $GEMINI_API_KEY = "AIza..."'
```

Note: as of v0.5, `/act.storyboard` no longer calls Claude — the agent writes the storyboard text itself following the protocol the action returns. No `ANTHROPIC_API_KEY` needed.

## System Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| `python3` (>= 3.10) + `pillow` | 2×2 grid composition in `grid.sh` | `pip install Pillow` |
| `jq` | JSON response parsing | `apt: jq` / `brew: jq` |

## Output location

All generated files land in `~/.string/users/default/apps/instatoon/out/<title>/`:

```
out/<title>/
├── character.png            # Single character reference sheet
├── storyboard.txt           # N-cut script (you write it; render reads it)
├── cut-1.png ... cut-N.png  # Rendered cuts
├── grid-1,2,3,4.png         # 2×2 grid (1 per /act.grid call)
└── bundle/                  # After /act.export — upload-ready set
    ├── (all of the above, copied)
    ├── caption.txt
    └── manifest.json
```

One app, many comic series — each `--title` is its own subfolder.

## Cost per instatoon (12 cuts)

| Stage | Service | Approx |
|---|---|---|
| Character ref | Gemini 3 Pro Image | $0.04 |
| Storyboard | local (the agent writes it) | $0 |
| 12 cuts render | Gemini 3 Pro Image × 12 | $0.48 |
| Grid composition (3 grids) | local Python (PIL) | $0 |
| Export bundle | local bash | $0 |
| **Total** | | **~$0.52** |

For a 4-cut single-grid version: ~$0.20.

## Prompt tips

When writing character descriptions:
1. **Mention species / identifying trait** — e.g. "a snowman character", "a golden retriever puppy"
2. **Express emotion through action** — never "she is sad", always "a tear rolls down her cheek"

These two rules alone produce dramatically more consistent and expressive output.

## Style + tone

Two tuning knobs on top of the structural workflow:

- `--style` (visual) — applied at character ref, storyboard visual-note hints, every rendered cut.
- `--tone` (narrative voice) — applied at storyboard text only.

Both default to `soft pastel kawaii` + `warm conversational blog voice` for a generic kawaii instatoon. Override per toon for noir, minimalist, kids comic, etc. See README for preset table.

**Consistency rule:** within one `--title` series, pass the same `--style` to `/act.character`, `/act.storyboard`, and every `/act.render` — otherwise the character ref and rendered cuts drift visually.

## Multi-language note

Storyboard text follows whatever language you write `--topic` and `--tone` in. A Korean topic produces Korean speech bubbles; an English topic produces English ones. Example for English:
```
/act.storyboard --title T --topic "..." --tone "casual english blog voice"
```
