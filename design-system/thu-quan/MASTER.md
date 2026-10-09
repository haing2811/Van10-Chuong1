# MASTER.md — "Thư quán cổ" (Thu Quan) design system

Source of truth for every visual decision on this site. Style brief (`style-brief.md`)
wins on style; `ui-ux-pro-max` wins on usability rules; `design-taste-frontend`
(taste-skill) supplies anti-slop judgment with the two overrides noted below.
Content, structure, and tech rules in `claude-code-prompt.md` are unchanged.

- Skill names that worked: `design-taste-frontend`, `ui-ux-pro-max`,
  `full-output-enforcement` (all invoked by exact name, all loaded).
- The ui-ux-pro-max generator script could not run in this environment (no shell
  or Python execution), so this file is authored directly from the skill
  architectures (three-layer tokens, usability priorities, pre-delivery checks).
- Dials: `DESIGN_VARIANCE = 8`, `MOTION_INTENSITY = 7`, `VISUAL_DENSITY = 3`.
- Overrides of taste-skill defaults: (1) stack is plain HTML/CSS/vanilla JS, no
  React/Tailwind/Motion, because the site must run from `file://` with no build
  step; (2) the premium-consumer beige ban is lifted because aged paper IS the
  brief, but the paper must be textured and uneven, never a flat cream default.

## 1. Concept (chosen, see Concepts at the end): "Cuộn kể chuyện"

Each of the three tabs (Đọc, Viết, Nói và nghe) is one handscroll. The home
screen is a rack holding three scrolls. Opening one unrolls it; reading travels
down its length. Sections inside a tab are passages of the same scroll, marked by
small hanging câu đối tags on threads at the side (the section navigator). Light
mode is the same room by day; dark mode is the same room by lamplight.

## 2. Primitive tokens (raw values, rarely change)

```css
:root {
  /* Paper scale: luminous center to tea-stained edge */
  --paper-100: #f2e7c9;
  --paper-200: #eadfc0;
  --paper-300: #ddcda4;
  --paper-400: #c9b183;
  --paper-500: #a98f5f;

  /* Desk scale (page surroundings): day */
  --desk-100: #6b543a;
  --desk-200: #4a3a27;
  --desk-300: #332818;

  /* Night scale (dark mode room) */
  --night-100: #2a2114;
  --night-200: #1c160d;
  --night-300: #14100a;
  --night-ink: #ece0c3;

  /* Ink scale */
  --ink-900: #241c12;
  --ink-700: #2b2118;
  --ink-500: #5a4f3d;
  --ink-300: #8a7c64;

  /* Rare accents */
  --seal-600: #9c3226;
  --seal-500: #b04432;
  --gold-500: #a8842f;
  --gold-300: #c8ab63;
  --jade-700: #3f5f52;
  --torch-500: #e08a3c;

  /* Type */
  --font-display: "Playfair Display", "Noto Serif", Georgia, "Times New Roman", serif;
  --font-body: "Noto Serif", Georgia, "Times New Roman", serif;
  --font-ui: "Be Vietnam Pro", -apple-system, "Segoe UI", sans-serif;
  --font-han: "Kaiti SC", "STKaiti", "KaiTi", "SimSun", serif;

  /* Space (reading-first, density 3: generous) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;
  --space-16: 4rem;
  --space-32: 8rem;
  --measure: 65ch;

  /* Shape: one system. Scroll corners are square; hanging tags are soft. */
  --radius-tag: 10px;
  --radius-seal: 4px;

  /* Motion */
  --dur-instant: 120ms;
  --dur-brush: 480ms;
  --dur-unroll: 800ms;
  --ease-settle: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-press: cubic-bezier(0.34, 1.4, 0.64, 1);
}
```

## 3. Semantic tokens (meaning; these are what components use)

```css
:root {
  --surface-desk: var(--desk-200);
  --surface-scroll: var(--paper-200);
  --surface-scroll-lit: var(--paper-100);
  --surface-tag: var(--paper-100);
  --surface-scrim: rgb(36 28 18 / 0.55);
  --text-ink: var(--ink-700);
  --text-quiet: var(--ink-500);
  --text-faint: var(--ink-300);
  --line-hair: var(--gold-500);
  --line-soft: var(--paper-400);
  --state-seal: var(--seal-600);
  --state-info: var(--jade-700);
  --focus-ring: var(--seal-500);
}
html[data-theme="dark"] {
  --surface-desk: var(--night-300);
  --surface-scroll: #3a2f1d;
  --surface-scroll-lit: #4a3c24;
  --surface-tag: var(--night-100);
  --surface-scrim: rgb(10 7 4 / 0.62);
  --text-ink: var(--night-ink);
  --text-quiet: #c9b98f;
  --text-faint: #9a8a68;
  --line-hair: var(--gold-300);
  --line-soft: #5a4c30;
  --state-seal: #d46954;
  --state-info: #9dc0ae;
  --focus-ring: var(--torch-500);
}
```

Contrast notes (AA required, verified pairs): `--text-ink` on `--surface-scroll`
is ~11:1 light, ~10:1 dark. `--text-quiet` on `--surface-scroll` is ~6:1 light
and ~5:1 dark. `--state-seal` on scroll is ~5.4:1 light. `--state-info` is the
deep jade `#3f5f52` precisely so quiet info text passes; the brighter jade is
never body text. Gold is hairlines and ornament only, never text. In dark mode,
body text always sits on the lamplit scroll panel or a steady scrim, never on
bare glow.

## 4. Typography

- Display (`.display`, h1/h2): Playfair Display 600/700, italic of the same
  family for emphasis only. Not Fraunces, not Instrument Serif. Diacritics test
  `Ữ Ặ Ẫ Ộ Ỳ Ằ Ể` must render in every shipped weight; fallbacks Noto Serif,
  Georgia, Times New Roman all carry Vietnamese.
- Body: Noto Serif 400/600, line-height 1.75, max-width `--measure`. Long
  passages (Chữ người tử tù) set slightly larger with extra leading.
- UI labels, buttons, inputs, tags: Be Vietnam Pro 500/700, small, quiet.
  Already the project font; it is Vietnamese-native.
- Han ornament (`讀寫說聽印`): `--font-han` local CJK stack, always
  `aria-hidden="true"`, never downloaded, never content. No brush webfont is
  shipped: none verified for Vietnamese, so brush character comes from SVG
  stroke-drawing technique, not from a font file.
- Vertical writing: `writing-mode: vertical-rl` allowed only for short
  decorative labels and the hanging tag titles, never for readable content.

## 5. Texture (the anti-flat-paper kit; static, cheap, no layout cost)

- Paper grain: one inline SVG `feTurbulence` data-URI tile, low opacity,
  applied to scroll surfaces. Decorative overlay grain, if animated at all, is a
  single fixed `pointer-events: none` layer shifting a few pixels very slowly.
- Tea-stained edges: layered radial/linear gradients darkening toward scroll
  edges plus an inset burnt-edge shadow. The scroll center (`--surface-scroll-lit`)
  catches the light; edges fall to `--paper-400/500`.
- Desk: deep warm brown with a faint wood-fiber gradient. Dark mode desk is
  near-black lacquer with a warm torch glow radial that follows the reading
  position area (a soft static pool behind the active passage, plus a very slow
  flicker at low amplitude; fully static under reduced motion).
- Seals: slightly rotated squares with uneven edges (border-radius jitter via
  `border-radius: 42% 58% ...` organic values), seal-red with paper-colored
  glyph, pressed with a soft spread ring on arrival.

## 6. Layout: the scroll, the rack, the tags

- Home: the rack. Three scroll objects (Đọc 讀, Viết 寫, Nói và nghe 說/聽）
  hung side by side, asymmetric (Đọc foremost, slightly lower, larger; the
  others recede into shadow). Each shows its name, a one-line description, and
  real progress (brush stroke). Choosing one unrolls it.
- Reading page: one vertical scroll. Wooden roller bars top and bottom (pure CSS:
  rounded bars with end knobs), paper between. Passages flow in mixed rhythms:
  wide full-bleed moments for big texts, narrow quiet columns for study notes,
  margin-note passages beside the text like manuscript annotations, vertical
  ornaments in margins. Chữ người tử tù passages go cinematic: darker panel,
  torchlit, paced reveals, distinct from the rest.
- Section navigator: hanging câu đối tags on threads at the reading side. Each
  tag is a real link (`#doc/van-ban-5`), scrollspy marks the current passage
  (tag swings forward, ink darkens, a small seal dot appears; never color-only,
  the active tag also gains weight and position). Threads sway slightly on touch
  (transform only). Mobile: tags collapse into the top roller bar as a compact
  horizontal strip of short titles, no default scrollbar look, momentum scroll
  with snap off (never trap scroll).
- Scroll progress: a brush line down the reading edge that draws itself with
  scroll position (CSS `animation-timeline: scroll()` where supported, with an
  IntersectionObserver fallback updating the same property), plus a small seal
  marking position. Native wheel, trackpad, touch, keyboard (arrows, Page
  Up/Down, Home/End, Space), and screen readers all keep working. No
  scroll-jacking, no trapped scroll, no fake scroll containers.
- No default scrollbar look anywhere: scrollbars that must exist (tag strip,
  search results, textareas) are restyled to hairline gold tracks with small
  roller-knob thumbs via `::-webkit-scrollbar` plus `scrollbar-width: thin` with
  matching colors.

## 7. Motion language: ink, paper, brush, light

Only transform, opacity, clip-path, and cheap filters. Every animation has a
`prefers-reduced-motion` alternative (instant or one gentle fade, no travel).
Heavy effects lazy-start via IntersectionObserver and stop when the tab hides.

1. First load: the title writes itself stroke by stroke (SVG `stroke-dasharray`
   on a brush-drawn title underline flourish, not on the text), paper warms in,
   a seal presses last with `--ease-press` overshoot.
2. Tab switch: the current scroll rolls up (clip-path inset from the bottom
   plus slight upward travel) while the new one unrolls; spatial, never a
   cross-fade.
3. Section move: ink-bloom reveal from the click point (clip-path circle expand
   at click coordinates) or the scroll gliding along its length; the old passage
   leaves the way it came.
4. Reading reveals: passages soak in like ink (opacity plus a 2px blur settling
   to 0, under 300ms, staggered only where sequence tells the story).
5. Answer reveal: the hidden slip pulls out and unfolds (grid-rows 0fr to 1fr
   plus clip-path), never a bare toggle.
6. Quiz correct: seal presses down with small impact and soft spread ring;
   incorrect: a gentle ink blot and a hint. Feedback is never color-only (icon
   plus words plus shape).
7. Speaking timer: an incense stick burning down (scaleY on the stick, ash tip,
   thin smoke line via animated dash) plus a plain numeric time.
8. Progress: the edge brush stroke draws itself, tied to real scroll position.
9. Hover/focus/press: ink spreading under the element (radial background bloom)
   and a 1px pressed settle (`translateY(1px)` / `scale(0.98)`); focus rings are
   visible ink rings (`--focus-ring` outline), never removed.
10. Idle: drifting mist and dust in the light at very low intensity, paused when
    the tab is hidden, off under reduced motion.

No animation library is shipped. CSS scroll-driven animations, the Web Animations
API, and IntersectionObserver cover moments 1-10; this keeps `file://` working
with zero network dependency and nothing to fail to load.

## 8. Components (every one reinvented; browser defaults banned)

Tabs/rack scrolls, hanging tag navigator, roller bars, brush buttons (ink-fill
buttons with spread press; ghost buttons as hairline gold frames), brush-line
range sliders with bead handles, passage viewer, progress brush stroke, incense
timer, answer slips, seal quiz feedback, flashcards as folded slips, Chú ý notes
as margin annotations with red margin rules, definition pops as unrolled mini
slips, comparison and self-evaluation tables as ruled manuscript tables (ruled
rows, no boxed grid, no filled score tracks; Dat/Chua dat as seal-stamp radios),
tooltips and glossary pops, modal as a laid-flat slip on the desk, search
(Ctrl/Cmd+K, results as slip list), day/night lamp control and text-size control
as desk objects, loading (brush draws then lifts) and empty states (an unmarked
slip with guidance), section headers with hairline gold rules and Han ornaments,
custom scrollbars, visible focus rings. Different content gets different physical
forms; no wall of identical boxes.

## 9. Copy hygiene

No builder notes in the interface. Exactly one small draft stamp per
section/card, styled as a faded pencil-grey stamp in the site language, tied to
`source: "draft"` in data. Interface text short, warm, Vietnamese. Zero
em-dashes anywhere (taste-skill pre-flight).

## 10. Guardrails (never traded away)

- 5-second orientation: rack names the three scrolls; every reading page shows
  where you are, a way back to the rack, and the next passage.
- Readable long text: `--measure` line length, AA contrast, steady background
  behind paragraphs, generous spacing.
- Keyboard, mouse, trackpad, touch, phone. Ornaments shrink or vanish before
  readability suffers. Touch targets 44px minimum.
- Hash routes and back button keep working (`#doc/van-ban-5` style preserved).
  Position and progress visible. Anchor IDs, route scheme, and localStorage keys
  from the current build are preserved (overhaul visuals, keep IA).

## Concepts (brief step 2; three genuinely different directions)

**A. Cuộn kể chuyện (handscroll journey, chosen).** Home: a rack of three
scrolls; reading: one vertical scroll unrolling downward with roller bars;
sections: passages marked by hanging câu đối tags with scrollspy; progress: a
brush line drawing down the reading edge. Tab switch: roll up one scroll,
unroll another. Chữ người tử tù: a darker torchlit length of the same scroll.

**B. Thư án (writing desk from above).** Đọc/Viết/Nói và nghe as objects on a
desk (bound book, brush with inkstone, lantern bell); choosing one glides it to
the center while others recede into shadow; sections live inside the chosen
object as pages, grindings, or chimes. Rich, but risky on phones (objects need
room) and harder to keep keyboard order and hash depth obvious.

**C. Sách gấp under torchlight (folding book).** Content on accordion folds that
turn in 3D on section change, whole site torchlit with light pooling on the
active fold. Most cinematic, but 3D folds threaten readability, perform worst on
mid-range phones, and punish reduced-motion users with the largest fallback gap.

Choice, in six lines: A is the boldest concept that still passes every
guardrail. It turns navigation itself into the metaphor (unrolling, passages,
tags) instead of decorating a docs layout. It is inherently vertical, so the
phone adaptation is natural, not a stacked compromise. It preserves the
approved single-scroll plus side-rail behavior and hash scheme with the least
invention. Its motion (unroll, bloom, seal press) is all transform/clip-path
work that stays smooth on mid-range phones. B and C spend their novelty on
spatial arrangements that fight small screens, keyboards, and reduced motion.
