---
name: instatoon
namespace: stringhub
version: 0.5.0
description: Topic → multi-cut Instagram comic (인스타툰). Per-toon style+tone, multiple series per app, the agent writes the storyboard itself, Gemini renders the cuts. Inspired by 눈오지 작가's gpters case study.
tags: [creator, instatoon, comic, instagram, korean, gemini]
type: app
requires: [GEMINI_API_KEY]
default: character
---

[!nav:main](./nav/main.md)
[!requirements](./requirements.md)

# instatoon

여러 만화를 한 앱에서 만들고, **각 만화별로 style/tone 조절** 가능.

```
/act.character  --title T → out/T/character.png  (--style 적용)
/act.storyboard --title T → out/T/storyboard.txt (--tone + --style 적용)
/act.render     --title T --cut K → out/T/cut-K.png (--style 적용)
/act.grid       --title T --cuts "1,2,3,4" → out/T/grid-*.png (style 영향 X)
/act.export     --title T → out/T/bundle/
```

`--title`은 모든 액션에 *required*. `--style`/`--tone`은 *optional* — 안 주면 기본 (kawaii + 친근한 일기체).

## 두 knob

| Knob | 어디서 쓰임 | 기본값 |
|---|---|---|
| `--style` | character ref 그림, render 컷 그림, storyboard 시각 메모 hint | `soft pastel kawaii, clean line art, light shadow` |
| `--tone` | storyboard 문장 톤 (나레이션/대사/행동 문체) | `친근한 일기체` |

**일관성 규칙:** 한 만화 시리즈 안에서는 character/storyboard/render에 **같은 style** 넘기는 게 좋음 (다른 style이면 캐릭터 ref와 컷이 어색하게 안 맞을 수 있음).

## 스타일 프리셋 예시

| 별명 | `--style` | `--tone` |
|---|---|---|
| 기본 (kawaii) | `soft pastel kawaii, clean line art, light shadow` | `친근한 일기체` |
| 미니멀 | `minimalist, monochrome ink wash, lots of white space` | `담담한 회고체` |
| 누아르 | `noir, high-contrast black & white, dramatic shadows` | `차분한 독백체` |
| 신문만화 | `vintage newspaper comic strip, sepia tone, halftone shading` | `풍자체` |
| 키즈 | `bright primary colors, simple bold shapes, kid-friendly` | `동심체, 의성어 많이` |
| 수채화 | `soft watercolor, painterly, warm color palette` | `서정적 산문체` |

## 컷 구조 (N컷 컨벤션)

```
컷 1   : 썸네일 — 후킹 (큰 텍스트, 강한 감정)
컷 2..N-1 : 본문 — 이야기 전개
컷 N   : CTA   — 좋아요/팔로우/공유 유도
```

## Workflow (LLM 기준)

1. `/act.character --title T --name X --description "..." [--style "..."]` — 1회
2. `/act.storyboard --title T --topic "..." --cuts 12 [--tone "..."] [--style "..."]` — 1회. **결과 검토.**
3. `/act.render --title T --cut K [--style "..."]` — N번 (백그라운드 sequential)
4. `/act.grid --title T --cuts "1,2,3,4"` — N/4번
5. `/act.export --title T --caption "..."` — 1회

## 사용 예시

**기본 (kawaii):**
```
TITLE=marathon
string app:instatoon "/act.character --title $TITLE --name 시명 --description '귀여운 45세, 안경, 턱수염, 카라티'"
string app:instatoon "/act.storyboard --title $TITLE --topic '...' --cuts 12"
# render + grid + export (style 기본)
```

**커스텀 스타일 (누아르):**
```
TITLE=noir-detective
STYLE="noir, high-contrast black & white, dramatic shadows"
TONE="차분한 독백체"
string app:instatoon "/act.character --title $TITLE --name 도진 --description '40대 형사' --style \"$STYLE\""
string app:instatoon "/act.storyboard --title $TITLE --topic '...' --tone \"$TONE\" --style \"$STYLE\""
# render: 같은 style 계속
for k in 1..12: string app:instatoon "/act.render --title $TITLE --cut $k --style \"$STYLE\""
```

## Prompt 팁 (눈오지 사례)

캐릭터 생성 시:
1. **종/식별 특징 언급** ("눈사람", "골든리트리버")
2. **감정을 행동으로** ("슬프다" → "눈에서 눈물이 또르르")

---

```act.character
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Character reference sheet for instatoon, white background, single character: {description}. Character name: {name}. Visual style: {style}. Show the character in a neutral pose, expressing emotion through body language. High consistency, recognizable silhouette."}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":{"imageSize":"1K","aspectRatio":"1:1"}}}'
  title, -T: string (required) "Toon slug (folder name)"
  name, -n: string (required) "Character name"
  description, -d: string (required) "Visual description (mention species/traits)"
  style, -y: string "Art style — match storyboard/render for consistency" = "soft pastel kawaii, clean line art, light shadow"
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
  topic, -t: string (required) "툰의 주제/내용"
  cuts: number "총 컷 수" = "12"
  character, -c: string "캐릭터 이름 + 짧은 설명" = "{character_name} ({character_description})"
  tone, -o: string "문체 톤" = "친근한 일기체"
  style, -y: string "비주얼 스타일 (시각 메모 generation 가이드)" = "soft pastel kawaii, clean line art, light shadow"
```

```act.storyboard.response
# 📋 Storyboard writing protocol — {title}

**You (the calling LLM) write the storyboard yourself, then save to:**
`~/.string/users/default/apps/instatoon/out/{title}/storyboard.txt`

## Parameters

- **Topic:** {topic}
- **Cuts:** {cuts}
- **Character:** {character}
- **Tone (문체):** {tone}
- **Style hint (시각 메모용):** {style}

## Structure (반드시 따르기)

- 컷 1: 썸네일. 후킹 한 문장. 큰 감정, 강한 표정.
- 컷 2~{cuts}-1: 본문 (시작 → 갈등 → 절정 → 해결 흐름)
- 컷 {cuts}: CTA (좋아요/팔로우/공유 요청)

## Output format (필수 — 모든 컷이 이 정확한 형식)

```
## 컷 N
- 나레이션: <컷 상단에 들어갈 자막. 1문장. 톤 반영.>
- 대사: <캐릭터가 말풍선으로 말하는 내용. 1-2문장. 톤 반영. 없으면 "없음">
- 행동: <감정을 *행동*으로 표현. 1문장. 예: 눈에서 눈물이 또르르>
- 시각 메모: <배경/소품/구도. 비주얼 스타일과 어울리게. 그림에만 반영. 1문장.>
```

## Rules

- 모든 컷의 캐릭터는 동일인. 일관성 유지.
- 감정은 직접 서술 X. 행동으로만 표현 (눈오지 핵심 팁).
- 한국어로 작성.
- 출력은 컷 1부터 컷 {cuts}까지만. 헤더나 부연 설명 없이.
- 톤({tone})을 나레이션/대사에 일관되게 반영.

## Action — what you do next

1. Write the storyboard text following the structure + format + rules above
2. Save with the Write tool to:
   `~/.string/users/default/apps/instatoon/out/{title}/storyboard.txt`
3. (Optional) Self-review: 컷 분배가 적절한가? 톤이 일관된가? 시각 메모가 style과 매치되는가?

## Why you write it (not an API call)

- You have full context of the user's intent / previous decisions
- No extra cost (~$0.05/storyboard saved)
- No API latency — instant
- Direct control: easy to iterate or override

next: /act.render --title {title} --cut 1 --style "{style}", ... --cut {cuts}
```

---

```act.render
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"inlineData":{"mimeType":"image/png","data":"{character|base64file}"}},{"text":"You are illustrating an instatoon (Instagram comic). Render ONLY cut #{cut}. Match the character in the reference image exactly: same colors, proportions, hairstyle, glasses, facial hair, clothing.\n\n# Visual style (use throughout)\n{style}\n\n# Text rendering rules (CRITICAL)\n- Narration (나레이션) → render as a clean Korean caption banner at the TOP of the panel.\n- Dialogue (대사) → render the EXACT Korean text inside a comic-style speech bubble (말풍선) next to the character. If 대사 is \"없음\", do NOT draw a speech bubble.\n- Visual memo (시각 메모) → informs composition, background, props. Never draw this text — only the scene it describes.\n- Emotion: show it through facial expression + body language + props. Never draw labels like \"슬픔\" or \"기쁨\".\n- Cut 1 (썸네일): add a LARGE hook text overlay (the 나레이션 line, oversized).\n- Last cut (CTA): include subtle 좋아요/팔로우 visual hint per 시각 메모.\n\n# Format\n1:1 square, white or light textured background (unless style dictates otherwise).\n\n# Storyboard (use ONLY the section for cut #{cut})"},{"text":"{storyboard|file}"}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":{"imageSize":"1K","aspectRatio":"1:1"}}}'
  title, -T: string (required) "Toon slug"
  cut, -c: number (required) "Cut number"
  style, -y: string "Visual style — MUST match character ref's style for consistency" = "soft pastel kawaii, clean line art, light shadow"
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

next: /act.render --title {title} --cut <next>  ·  after final cut: /act.grid --title {title} --cuts "1,2,3,4"
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

next: manually upload the bundle. ·  /act.character --title <new-toon> for next series.
```
