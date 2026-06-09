# instatoon

Multi-cut Instagram comic (인스타툰) generator with per-toon **style + tone** customization. Each comic is a *titled* series — character → N-cut storyboard (you write it) → N rendered cuts → 2×2 grids → upload-ready bundle. All outputs for one comic live in `out/<title>/`.

## v0.5 — storyboard is now your job

Previously `/act.storyboard` called Claude Opus to generate the storyboard text. **As of v0.5 you (the calling LLM) write the storyboard yourself** and save it to disk. The action returns a writing protocol (structure + format + rules + parameters). Reasons:

- You have full context of the user's intent
- No extra API cost (~$0.05/storyboard saved)
- Direct control — easy to iterate, override, fix on the spot
- No external dependency (`ANTHROPIC_API_KEY` no longer required)

Workflow is otherwise unchanged.

Inspired by [눈오지 작가's gpters case study](https://www.gpters.org/nocode/post/will-close-my-instatoon-nbCpy3th9wDtk6j) where 1000 toons were created in 3 days using GPT Image2.

## Two tuning knobs

| Knob | Affects | Default | Where applied |
|---|---|---|---|
| `--style` | Art style of the comic | `soft pastel kawaii, clean line art, light shadow` | character ref + storyboard 시각 메모 + each rendered cut |
| `--tone` | Narrative voice in storyboard text | `친근한 일기체` | storyboard prompt (controls 나레이션/대사/행동 phrasing) |

Both are *optional* on every action. Defaults give you a kawaii instatoon. Override for a noir thriller, minimalist illustration, kids comic, etc.

**Consistency rule:** within one toon series, pass the **same `--style`** to character / storyboard / render. The character ref encodes the look visually; if a later cut uses a different style hint, the result drifts from the ref.

## Preset palette (pick one, override individually)

| Vibe | `--style` | `--tone` |
|---|---|---|
| **kawaii** (default) | `soft pastel kawaii, clean line art, light shadow` | `친근한 일기체` |
| **minimalist** | `minimalist, monochrome ink wash, lots of white space` | `담담한 회고체` |
| **noir** | `noir, high-contrast black & white, dramatic shadows` | `차분한 독백체` |
| **newspaper comic** | `vintage newspaper comic strip, sepia tone, halftone shading` | `풍자체` |
| **kids** | `bright primary colors, simple bold shapes, kid-friendly` | `동심체, 의성어 많이` |
| **watercolor** | `soft watercolor, painterly, warm color palette` | `서정적 산문체` |

## Quick start

```bash
# One-time setup
string app:instatoon '/set $GEMINI_API_KEY = "AIza..."'
# (no ANTHROPIC_API_KEY needed in v0.5 — you write the storyboard yourself)
```

### Example 1 — Default kawaii style

```bash
TITLE=marathon

string app:instatoon "/act.character --title $TITLE --name 시명 --description '귀여운 45세 아저씨, 안경, 까끌한 턱수염, 카라티'"

# Storyboard: action returns guidelines. YOU write the file using Write tool.
string app:instatoon "/act.storyboard --title $TITLE --topic '45세 시명 아저씨가 광교호수공원에서 매일 아침 러닝, 풀코스 마라톤 sub-3 달성' --cuts 12"
# (LLM reads the protocol, writes 12-cut storyboard, saves with Write tool to:
#  ~/.string/users/default/apps/instatoon/out/marathon/storyboard.txt)

# Render 12 cuts (reads storyboard.txt at render time)
for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  string app:instatoon "/act.render --title $TITLE --cut $k"
done

string app:instatoon "/act.grid --title $TITLE --cuts '1,2,3,4'"
string app:instatoon "/act.grid --title $TITLE --cuts '5,6,7,8'"
string app:instatoon "/act.grid --title $TITLE --cuts '9,10,11,12'"

string app:instatoon "/act.export --title $TITLE --caption '45세 마라톤 sub-3 도전기 🏃‍♂️ #마라톤 #광교호수공원 #서브3'"
```

### Example 2 — Custom noir style

```bash
TITLE=noir-case
STYLE="noir, high-contrast black & white, dramatic shadows, cinematic angles"
TONE="차분한 독백체, 짧고 단호한 문장"

string app:instatoon "/act.character --title $TITLE --name 도진 --description '40대 형사, 트렌치코트, 짧은 머리, 피로한 눈' --style \"$STYLE\""
string app:instatoon "/act.storyboard --title $TITLE --topic '신참 형사 도진이 7년 전 미제 사건의 새 단서를 발견하고 진실에 다가가는 이야기' --cuts 12 --tone \"$TONE\" --style \"$STYLE\""

for k in 1 2 3 4 5 6 7 8 9 10 11 12; do
  string app:instatoon "/act.render --title $TITLE --cut $k --style \"$STYLE\""
done

string app:instatoon "/act.grid --title $TITLE --cuts '1,2,3,4'"
# ... etc
string app:instatoon "/act.export --title $TITLE --caption '신참 형사 도진, 7년만의 진실 ⚖️ #누아르 #미제사건'"
```

## Pipeline

```
[topic + character + title + (style + tone)]
        │
        ▼
/act.character    →  out/<title>/character.png       (--style applied)
        │
        ▼
/act.storyboard   →  out/<title>/storyboard.txt      (--tone + --style applied)
        │
        ▼  (review storyboard before continuing!)
        │
/act.render × N   →  out/<title>/cut-1.png ... cut-N.png   (--style applied per cut)
        │
        ▼
/act.grid × ⌈N/4⌉ →  out/<title>/grid-<cuts>.png    (pure composition, style not applicable)
        │
        ▼
/act.export       →  out/<title>/bundle/             (everything + caption + manifest)
```

## Why `--title`?

One app can host many comic series. Each series has its own subfolder:

```
out/
├── marathon/
│   ├── character.png, storyboard.txt
│   ├── cut-1.png ... cut-12.png
│   ├── grid-1,2,3,4.png ... grid-9,10,11,12.png
│   └── bundle/
└── noir-case/
    ├── character.png, ...  ← different style, same app
    └── ...
```

`--title <slug>` is required on every action so files land in the right folder.

## Why these prompt rules (gpters case study)

The 눈오지 author identified 3 properties of recent image-gen models that make instatoon automation viable:

1. **Consistency** — A character reference can be reused across cuts and stay recognizable.
2. **Emotion via action** — Models render emotional states better when described as physical actions (눈물 흘림 vs 슬픔).
3. **Prop usage** — Models incorporate small props/objects well, adding scene richness.

This app encodes:
- Character action mentions species/identifying trait
- Storyboard prompt forces "행동:" field per cut, banning direct emotion descriptions
- Render prompt explicitly distinguishes 나레이션 (top caption), 대사 (speech bubble), 시각 메모 (composition only)
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

## Output structure (after full cycle)

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
| `/act.storyboard` | `--title`, `--topic` | `--cuts`, `--tone`, `--style`, `--character` | **writing protocol** → LLM writes `out/<title>/storyboard.txt` |
| `/act.render` | `--title`, `--cut` | `--style`, `--character`, `--storyboard`, `--filename` | `out/<title>/cut-<N>.png` (Gemini API) |
| `/act.grid` | `--title`, `--cuts` (4-tuple) | — | `out/<title>/grid-<cuts>.png` (local) |
| `/act.export` | `--title` | `--caption` | `out/<title>/bundle/` (local) |

## Reinstalling after edits

Editing `work/apps_tmp/instatoon/string.md` does NOT auto-reinstall. After changes:

```bash
string /uninstall instatoon
string /install --app /home/chsjk/h1r_ai/work/apps_tmp/instatoon/
# Re-set keys (env may be cleared on uninstall)
string app:instatoon '/set $ANTHROPIC_API_KEY = "..."'
string app:instatoon '/set $GEMINI_API_KEY = "..."'
```

Handy alias:
```bash
alias rein-instatoon='string /uninstall instatoon 2>/dev/null; string /install --app /home/chsjk/h1r_ai/work/apps_tmp/instatoon/'
```

## Future work (v0.5+)

- Auto-upload via Instagram Graph API (Business account)
- Hook text overlay sizing improvements for cut 1
- Batch render (parallel API calls) for faster N-cut generation
- `/act.regenerate-cut --title T --cut K` for fixing one bad cut without redoing all
- Style preset shorthand (`--preset noir` instead of full string)
- Aspect-ratio option (1:1 default, 4:5 for feed, 9:16 for stories)
