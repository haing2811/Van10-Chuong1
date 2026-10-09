# STYLE BRIEF – "Thư quán cổ": a calligraphy scroll world on aged yellowed paper

This brief FIXES the visual concept and motion language of the whole site. It overrides the line in `claude-code-prompt.md` that says the design skills decide everything about the look. Content, structure and tech rules in `claude-code-prompt.md` stay as they are.

**This brief deliberately gives NO color values, NO font names and NO fixed layout.** It describes the world, the feeling, the behavior and the quality bar in words. The plugins (taste-skill and ui-ux-pro-max) must turn these words into concrete colors, fonts, layout and motion. If you catch yourself reaching for a generic default, stop and push further.

## 0. How to use the two plugins (do this first)

1. **Find the exact skill names. Do not guess.** Run `/skills` (or look inside the installed plugin folders) and write down the exact names provided by **ui-ux-pro-max** (expected `ui-ux-pro-max`) and **taste-skill** (main skill expected `design-taste-frontend`; others like `high-end-visual-design`, `minimalist-ui`, `full-output-enforcement` may also exist). If a name fails with "Unknown skill", do not retry variations: open the plugin folder, read its `SKILL.md` directly and follow it. Tell me which names worked.
2. **taste-skill dials** (state them in your notes): `DESIGN_VARIANCE = 8` (I want unusual, asymmetric, composed layouts), `MOTION_INTENSITY = 7` (rich, choreographed, but still calm), `VISUAL_DENSITY = 3` (spacious, made for reading). Use `full-output-enforcement` if available so nothing is left half-built.
3. **ui-ux-pro-max builds the design system** (needs Python 3). Run its design-system generator with keywords taken from section 2 (for example: `"calligraphy handscroll aged handmade paper ink wash classical oriental study reading immersive"`) and persist it as `design-system/thu-quan/MASTER.md` (use its `--persist` option). If its automatic suggestion drifts toward glassmorphism, neon, bento grid, dark SaaS or "clean dashboard", **this brief wins on style**. ui-ux-pro-max still wins on usability rules: contrast, touch targets, focus states, forms, reduced motion, responsive behavior.
4. Convert the result into design tokens (CSS variables) before building pages. Every color, font, radius, shadow, texture and duration comes from tokens.

## 1. What went wrong last time (do NOT repeat)

The first attempt looked like a generic documentation site: a dark page, a header with a search box, three pill-shaped tabs with a mint-green active state, a left sidebar list with a default scrollbar, and a stack of identical rounded cards that fade in. Motion was a few default fades. That is exactly what I do NOT want.

Banned unless you can justify it as part of the concept:
- header + left sidebar + stacked rounded cards layout; "docs site", "SaaS dashboard", "blog template", "Notion-like" looks
- pill/segmented tabs; default-looking buttons, inputs, checkboxes, selects
- **any default-looking scrollbar** anywhere (sidebar, panels, textareas, modals)
- the same fade-up on every element; generic hover color changes; generic loading spinners
- a bright accent color on a dark UI by default; purple/blue gradients; glassmorphism; emoji as icons
- the same card shape repeated for every kind of content

**Test:** if a screenshot of any page could belong to another website or a template, redo it.

## 2. The world of the site (describe, don't dictate)

Imagine a scholar's study long ago, late in the evening. A long hand-painted calligraphy scroll is being unrolled across a low writing desk. The paper is hand-made and old: yellowed, fibrous, slightly uneven, with tea-colored stains, soft burnt edges, a faint smell of ink and incense. Ink exists in many dilutions: dense lustrous black for the strokes that matter, grey washes for mist and distance, dry-brush streaks where the brush ran out. A few small red seals mark important moments, pressed unevenly the way real seals are. Old gold and a hint of jade appear only in fine details. A single lamp or torch gives warm, flickering light, like the scene in *Chữ người tử tù*: a dark cell, silk, ink, torchlight, three heads bent over a white cloth.

Mood: quiet, warm, literary, a little melancholic, dignified, tactile. It should feel handmade and physical, like a real object, never like a flat web template. This is Sino-Vietnamese classical culture (Nho học, thư pháp, thủy mặc, sách gấp, hoành phi, câu đối), the world of *Vang bóng một thời*. Decorative Hán characters are welcome as ornament only; all real content stays Vietnamese.

Light and dark: there must be a light mode (daylight on old paper) and a dark mode (the same room at night by lamplight). They are two times of day in the same world, not two inverted themes.

## 3. Color (described, not dictated)

You choose the exact values with the plugins. The description to honor:
- The dominant impression is **aged yellowed paper**, warm and slightly uneven, with darker tea-stained edges. Not flat beige, not cream-white, not orange.
- Text is **ink**: soft near-black with a brown warmth, never pure black. Secondary text is diluted ink.
- **Red** is rare and meaningful: seals and a few key moments only, the way a real seal is used. Never a UI accent for ordinary buttons.
- **Old gold** for hairlines and ornaments. A **faded jade or indigo** for quiet informational states only.
- Dark mode is warm: lacquer-brown / deep ink darkness, paper-colored text, and a flicker of torch orange as light, not as UI accent.
- Never a cold dark grey UI, never a mint/neon accent, never a rainbow.
- Hard constraint: body text keeps WCAG AA contrast against the paper and against the dark background.

## 4. Typography (described, not dictated)

- Headings have a calligraphic, brush-written or classical-engraved character, with real presence and scale contrast. Body text is a calm, readable serif for long reading. UI labels can be quieter and smaller.
- **Every font must render all Vietnamese diacritics correctly** (test "Ữ Ặ Ẫ Ộ Ỳ Ằ Ể" in every weight). If a brush font fails on Vietnamese, it may not be used for Vietnamese text.
- Large decorative Hán characters (brush style, semi-transparent or sealed in red) may be used only as ornament, only with characters you are sure about, always `aria-hidden`. Suggested: 讀 (Đọc), 寫 (Viết), 說 (Nói), 聽 (Nghe), 印 (seal). Do not write sentences in Chinese.
- Vertical writing is allowed for short decorative labels and section names, never for content people must read.

## 5. Layout: unusual on purpose, usable at first glance

I want a layout I have not seen on any website. Do not start from "header + sidebar + cards". Start from the physical world of section 2 and invent the structure of the site from it. The plugins should propose and decide. Seeds to get you thinking (use, combine or beat them, you are not limited to these):

- **The handscroll journey:** the chapter is one long scroll the reader travels along. Moving through content unrolls the scroll; the three tabs are three different scrolls or rolls on a rack that you pull out and unroll.
- **The writing desk (thư án):** Đọc, Viết, Nói và nghe are physical objects on a desk seen from above, for example a bound book, a brush with an inkstone, a lantern or bronze bell. Choosing one brings it to the center while the others recede into the shadows. Sections live inside the chosen object.
- **The folding book (sách gấp):** content lives on accordion-folded pages that fold open and closed in 3D; a section change is a fold turning.
- **The torch in the cell:** in dark mode, light pools around the active area and slowly flickers, with the rest of the page falling into soft darkness (only if readability and accessibility stay intact).
- **Hanging plates and vertical banners** (hoành phi, câu đối) as navigation, hung at different heights, swaying slightly when touched.
- Mixed reading rhythms: wide full-bleed moments for the big texts (especially *Chữ người tử tù*), narrow quiet columns for study notes, margin notes that sit beside the text like annotations on an old manuscript, vertical ornaments in the margins.
- *Chữ người tử tù* is the showpiece: give its four parts a distinctly cinematic treatment (the whole scene should feel different from the rest of the site, darker, lit by torchlight, paced like a story).

**Usability guardrails for an unusual layout** (these never get traded away):
- Within 5 seconds a new user knows where they are, what the three tabs are, and how to go back or move on. Use clear, labeled affordances; ornament must not hide navigation.
- Long text is comfortable to read: sensible line length, strong contrast, steady background behind paragraphs, generous spacing.
- It works with keyboard, mouse, trackpad and touch, and on a phone. On phones the concept adapts (it does not just stack desktop elements). Ornaments shrink or disappear before readability suffers.
- Hash routes and the browser back button keep working. Position and progress are visible.

## 6. Scrolling and navigation feel

- **No default scrollbar look anywhere.** Replace it with something that belongs to the world (for example a scroll-roller indicator, a brush line that fills as you read, or a position marked by a seal) while keeping normal scrolling behavior: wheel, trackpad, touch, keyboard (arrows, Page Up/Down, Home/End, Space) and screen readers all keep working. Never fake scrolling in a way that breaks these.
- Scroll position should *mean* something in the concept (unrolling, ink being laid down, a lamp moving along), and reading progress is visible.
- Smooth, physical-feeling movement; no scroll-jacking that fights the user, no trapped scroll.

## 7. Animation and transitions: the quality bar is high

The motion language is **ink, paper, brush and light**. Everything that moves should look like something that could physically happen with ink, paper, wood, thread or flame. Motion has a purpose: it explains where something came from, where it goes, or what just happened. Choreograph with intent: staggered sequences, anticipation, overshoot where a real object would, slow settle, varied easing. Not every element moves, and not every element fades up.

Signature moments to design properly (each one memorable):
1. **First load / entering the site:** a scroll unrolls or a brush writes the title stroke by stroke (SVG stroke drawing), the paper warms into view, a seal is pressed last.
2. **Switching tabs (Đọc / Viết / Nói và nghe):** a real spatial transition tied to the layout concept (unrolling a different scroll, pulling an object forward on the desk, turning a fold), not a cross-fade.
3. **Moving between sections inside a tab:** ink bloom or brush-wipe revealed from the click point (clip-path / mask), or the scroll sliding along its length; the old content leaves in a way that makes sense.
4. **Text reveal while reading:** lines or paragraphs appear like ink soaking in or being written, subtle and quick enough not to slow reading, triggered by scroll position.
5. **Revealing an answer:** the hidden slip is pulled out, unfolded or uncovered, not just toggled.
6. **Quiz result:** correct = a red seal presses down with a small impact and a soft ink spread; incorrect = a gentle ink blot and a hint, never harsh. Feedback is never color-only.
7. **Speaking timer:** an incense stick burning down with ash falling and a thin smoke line, plus a plain readable time.
8. **Progress:** a brush stroke that draws itself, or a scroll that unrolls further, tied to real progress.
9. **Hover, focus and press** on every interactive piece have physical feedback (ink spreading, a seal pressed, a thread swaying), never just a color swap.
10. **Idle atmosphere:** very slow background life (drifting mist, flickering lamp light, dust in the light, paper grain shifting a few pixels) at low intensity, paused when the tab is hidden and off with reduced-motion.

Techniques to use (pick the best for each moment): CSS `clip-path` and `mask` reveals, SVG `stroke-dasharray` brush drawing, SVG filters (`feTurbulence` + `feDisplacementMap`) for ink-bleed edges and paper grain, CSS scroll-driven animations (`animation-timeline: scroll()` / `view()`), the View Transitions API, Web Animations API, FLIP, small canvas effects for ink and smoke. You may use ONE small animation library from a CDN (for example GSAP with ScrollTrigger) if it clearly raises quality, but the site must stay fully usable if it fails to load, and must not need a build step. Add graceful fallbacks when a browser lacks a feature.

Performance and safety of motion: animate transform, opacity, clip-path and filters sparingly; no layout thrash; smooth on a mid-range phone; heavy effects are lazy-started and stoppable. **Every animation has a `prefers-reduced-motion` alternative** (instant or a gentle fade, no travel). Nothing flashes quickly. Ornaments never block clicks or shift layout.

## 8. Components (reinvent the look, do not just reskin)

Every interactive piece belongs to the world; nothing falls back to a browser default:
tabs/navigation, buttons, range sliders and any draggable control (a brush-line track with a bead or stone as handle, for example), carousels and page viewers, progress bars and rings, the speaking timer, checkboxes/radios/toggles, text inputs and textareas (for the 150-word paragraph and the outline builder), quiz and answer reveal, flashcards, cards and notes (Chú ý, definitions), tables (comparison, self-evaluation), tooltips and glossary pops, modal/lightbox, search (Ctrl/Cmd+K), light/dark and text-size controls, loading and empty states, dividers and section headers, scrollbars, focus rings.

Different kinds of content get different physical forms (a story summary is not shaped like a quiz or like a table). Vary scale and rhythm; avoid a wall of the same box.

## 9. UI copy hygiene

- Do not leak builder notes into the interface. Phrases like "Mục này chưa có trong outline", "source: draft", file names or instructions to me must never appear in the page text.
- Draft markers ("Nháp - cần duyệt") appear once per section or card, small and unobtrusive, in the visual language of the site (for example a faded pencil stamp). Never repeat the marker line by line, and never let it break the design. All of it stays tied to `source: "draft"` in the data.
- Interface text is short, warm and in Vietnamese.

## 10. Process and checkpoint

1. Load the plugins (section 0), generate `MASTER.md`.
2. **Concepts first:** write 3 genuinely different layout-and-motion concepts (each one short paragraph + a rough sketch in words of home, a reading page and the tab switch). Choose the boldest one that still passes the usability guardrails in section 5. Tell me which you chose and why in 6 lines. Do not wait for me here.
3. Build `styleguide.html` (plain HTML/CSS/JS, the same tokens), a living page that shows the palette, typography, every component from section 8 in light and dark, and a demo of the signature motions from section 7. Then build a working **prototype of the home screen + the tab switch + one reading section (Chữ người tử tù, part 1)** to prove the layout and the motion.
4. If you can run a headless browser (for example Playwright), take screenshots at phone and desktop widths and look at them honestly against section 1's test. If you cannot view images, say so and verify by inspecting the DOM and CSS. Fix what looks generic.
5. Give me a short summary: skill names that worked, tokens and fonts chosen, the concept, how to open the styleguide and the prototype. **Then stop and wait for my OK.** If I send feedback, change the styleguide and prototype first.
6. After my OK, build the full site from `outline.md` following `claude-code-prompt.md`, reusing the same tokens, components and motion. Do not add new visual ideas that were not in the approved styleguide.
7. Final check: every component matches the styleguide; text contrast passes AA in light and dark; no browser-default controls or scrollbars remain; reduced motion works; keyboard works; phone width works; works by double-clicking `index.html`.