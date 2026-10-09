# PROMPT: Study website – Ngữ văn 10 (Kết nối tri thức), Tập 1, Bài 1 "Sức hấp dẫn của truyện kể"

## 0. How to work (read first)

You are building a **static, interactive study website** (HTML + CSS + vanilla JS) for ONE chapter of a Vietnamese textbook.

**This prompt does NOT decide any UI or UX.** Layout, visual style, colors, typography, navigation patterns, component shapes, animations, interaction patterns and microcopy tone are decided by the design skills. Before writing any code:

1. **Use the installed plugins.** My Claude Code has these plugins enabled: **taste-skill**, **ui-ux-pro-max** (design) and **superpowers** (workflow: planning, task breakdown, verification). Check with `/plugin` (or look at the plugin list) which plugins are enabled, then use the skills that each plugin provides (look them up in each plugin's skills list and invoke them with the Skill tool). If another design plugin such as **impeccable** is also enabled, use it too. Do not rely on skills that are not provided by an enabled plugin.
   - **taste-skill and ui-ux-pro-max own all UI/UX decisions** (layout, style, colors, typography, navigation, interactions, animations). If their guidance conflicts, prefer ui-ux-pro-max for UX/accessibility and taste-skill for visual taste, and say which you chose.
   - **superpowers** guides how you work: plan before building, break work into steps, verify before claiming done.
   - Where this prompt says "design skills", it means the skills from these plugins. Where it names a feature (e.g. "answers can be revealed"), it only says the **function must exist**, not how it looks or is laid out.
2. Read `outline.md`, `outline-skeleton-bai1.md` and `sgk_van.pdf` (see section 1).
3. 3. Decide your own image slots and build images/images.manifest.js (see section 5). Do not search for image files, and do not draw or download any.
4. Create a task list. Build order: content data -> structure and routing -> the three tabs -> interactive functions -> QA. After step 2 give me a 5-line summary of the design direction the plugins' skills chose, then keep going without waiting.
5. Use exact tool names only: Read, Write, Edit, Glob, Grep, Bash. Never add a prefix like "default." or "functions.". Call exactly ONE tool per turn, never in parallel. If Grep fails, use Bash with grep or rg instead. Do not retry the same failing call; switch tool and continue.

Deliverable: a working web app I can open from `index.html` and deploy as static files (GitHub Pages / Vercel). No backend, no build tools, no frameworks.

## 1. Content authority (highest priority – applies to everything)

**Every piece of content on the site must follow `outline.md` (mine).** This rule overrides everything else in this prompt about content.

Source order when deciding what text goes on the site:

1. **`outline.md`** is the primary source. Use my wording. Do not rewrite, summarize away, merge or drop anything in it.
2. **Gaps:** if a section in `outline.md` is missing, unfinished, cut off, empty, or marked `→`, fill it using:
   - `outline-skeleton-bai1.md` for **what** the section must contain (its headings and the `→` slots show the required items), and
   - `sgk_van.pdf` (the textbook) for the **facts**: definitions, quotes, summaries, exercise questions, page numbers.
   Cross-check any fact against the PDF before putting it on the site. If the PDF does not contain it, do not invent it.
3. Anything you filled in yourself is marked in the data as `source: "draft"` (anything from my outline is `source: "outline"`), and the site must visibly flag draft items (a small "Nháp – cần duyệt" label; the design skills decide how it looks) so I can review them.
4. If `outline.md` and the textbook disagree, keep my version in the content and list the disagreement in the final report. If `outline.md` has a clear mistake (typo, non-existent word, wrong fact), fix it and list the fix.
5. Do not add literary analysis of your own beyond what outline/skeleton/PDF support. When you do need to write a bridging sentence, keep it short and neutral.
6. If `outline.md` has content that no section in this prompt covers, still put it on the site in the most fitting tab and tell me where.

**Coverage check (required):** create `COVERAGE.md` mapping every heading and bullet group of `outline.md` (and every skeleton item) to the place on the site where it appears, with its source (`outline` / `draft`). Any unmapped item = not done. List unmapped items in the final report.

When I edit `outline.md` later, re-run the coverage check and only change what changed.

Known issues to handle:
- Hán Việt Bài 3: the outline lists "hàn: hàn đớ", which is not a real word. Replace with correct words containing "hàn" and verify.
- The "Nói và nghe" section of the outline is cut off mid-sentence ("…một cách th"). Complete it from the textbook (pages 35-36).
- Verify Hán Việt meanings and quotes against the textbook.

## 2. Scope: tabs and required content

Three top-level tabs, matching the book (names fixed, everything else is the design skills' call):

| Tab | Label | Content |
|---|---|---|
| 1 | **Đọc** | Tri thức ngữ văn, Văn bản 1-3, Văn bản 4, Văn bản 5, câu hỏi từng văn bản, Kết nối đọc – viết, Thực hành tiếng Việt (Hán Việt) |
| 2 | **Viết** | Nghị luận phân tích, đánh giá một tác phẩm truyện |
| 3 | **Nói và nghe** | Giới thiệu, đánh giá nội dung và nghệ thuật một tác phẩm truyện |

Also include **Củng cố, mở rộng** and **Thực hành đọc (Tê-dê)** as sections where they fit best (inside one of the tabs or as an extra area; the design skills decide). Section order inside each tab follows `outline-skeleton-bai1.md`.

The full list of sections and items is in `outline.md` + `outline-skeleton-bai1.md`. The site must contain all of them. Do not leave a section out because it is hard to make interactive; a plain content section is fine.

## 3. Interactive functions that must exist

Only the **function** is required. How it is presented is not decided here.

- Answers to the book's questions can be hidden until the student chooses to see them; each answer is labeled as a suggestion. The student can type their own answer first and it is saved.
- Short self-test quizzes for Tri thức ngữ văn and per text (questions from the outline/skeleton/PDF).
- 150-word paragraph exercises (Kết nối đọc – viết): text input with word counter and saved draft.
- Hán Việt practice (Bài 1-4 from the outline): word meanings, replacing a Hán Việt word with a Vietnamese word, building words, spotting and fixing wrong usage.
- Writing support (tab Viết): the 4-step process, the reference essay with its margin notes tied to the matching parts, an outline-building tool (mở bài / thân bài / kết bài) that can be copied or exported, a checklist for the writing and revising rules, a self-review against the 5 requirements.
- Speaking support (tab Nói và nghe): structuring a talk into Mở đầu / Triển khai / Kết luận, sentence starters and transition words, a speaking timer, the 6-row self-evaluation table (Đạt / Chưa đạt) with saved state.
- Comparison tables from Củng cố, mở rộng that the student can fill in and then check against suggested answers.
- Progress saved locally (quiz results, checklist state, drafts, last position).
- Search across all content.
- Light/dark and text-size adjustment if the design skills judge them worthwhile.

## 4. Tech constraints (these are technical, not visual)

- **Plain HTML + CSS + vanilla JavaScript.** Classic `<script src>` files sharing one global namespace (e.g. `window.App`, `window.CONTENT`). Use ES modules only if you verify they work from `file://`. **NO React, Vue, Vite, npm, build step, frameworks or TypeScript.** The site must work by double-clicking `index.html` and from any static server.
- External resources: only Google Fonts and, if really needed, a small CDN library. Prefer zero dependencies; inline SVG for icons.
- Suggested structure (adjust if needed):
  ```
  index.html
  /css/      styles
  /js/       app.js (init + router), tabs, quiz, editor, timer, search, storage ...
  /content/  one .js file per section, assigning to window.CONTENT
  /images/   empty at first; I add files named in IMAGES_NEEDED.md + images.manifest.js
  ```
- **All content lives in `/content` files**, never hardcoded in HTML, so I can edit text without touching logic. Each content item carries `source: "outline" | "draft"`. Sanitize any injected HTML (prefer `textContent`).
- State: plain objects + `localStorage` through a small wrapper, every access in try/catch; site must still work with localStorage disabled.
- Routing: hash-based so every section is linkable and the back button works.
- Language: Vietnamese, `<html lang="vi">`. Fonts must fully support Vietnamese diacritics (test "Ữ, Ặ, Ẫ, Ộ, Ỳ").
- Respect `prefers-reduced-motion`. Keep the site usable with keyboard only and with sensible alt text; the design skills decide how.
- Performance: lazy-load images, set dimensions, render a section's DOM only when opened.

## 5. Images (the agent decides)

Read claude-code-prompt.md fully and follow it exactly. Start now.

Files in this folder:
- outline.md = my content. Everything on the site must follow it, in my wording.
- outline-skeleton-bai1.md = the list of what each section must contain.
- sgk_van.pdf = the textbook, for facts, quotes and exercise questions.
- images/ = empty. I will find the pictures myself.

Rules for this run:
1. Content: use outline.md first. If a part of it is missing, cut off, empty or marked "→", fill it using the skeleton (what to include) and the PDF (the facts). Do not invent anything the PDF does not support. Mark every item you filled in as source "draft" and show a visible "Nháp - cần duyệt" label on the site.
2. UI and UX: you do not decide them. Use the enabled plugins: taste-skill and ui-ux-pro-max decide layout, style, navigation and interactions; superpowers guides your planning and verification. Check /plugin to confirm they are enabled. Keep only the three tabs Đọc, Viết, Nói và nghe.
3. Images: do not search for image files, and do not draw, generate or download any. You decide where images go and pick a filename for each slot in images/. Every slot shows a placeholder with its filename and a one-line brief of what to find, until I add the file. Then write IMAGES_NEEDED.md as a shopping list for me: per slot the filename, where it appears, a specific description of what the image should show, search keywords in Vietnamese and English, orientation and size, licensing note, ordered by priority.
4. Tech: plain HTML, CSS and vanilla JS only. No frameworks, no npm, no build step. It must work by double-clicking index.html.
5. After the plugins' skills have chosen the design, give me a 5-line summary of the design direction, then keep going without waiting for me.
6. When done, give me COVERAGE.md, IMAGES_NEEDED.md, and the final report described in the prompt.
Work sequentially, no parallel subagents, read the PDF in small page ranges.

## 6. QA before you say you're done

- Opens and works from `index.html` directly (file://) AND from a static server. No console errors.
- Every item in `outline.md` and the skeleton is on the site (`COVERAGE.md` has no unmapped items).
- All `draft` items are visibly flagged; nothing was invented that the PDF does not support.
- Quotes, Hán Việt meanings and page numbers checked against the PDF.
- No broken-image icons. Every slot shows its file if present, otherwise a placeholder with filename and brief. IMAGES_NEEDED.md matches the manifest and every row is specific enough to search for.
- Hash routes work, back button works, no broken links.
- Works with localStorage disabled.
- Keyboard-only run-through of tabs, quizzes and image viewing works.
- Check the result on a phone-width and a desktop-width screen (the design skills define the layouts).

## 7. Final response format

Reply with: what you built (3 lines), how to run it (open `index.html`), the design direction the skills chose (5 lines), the list of outline fixes and outline-vs-textbook disagreements, unmapped items from `COVERAGE.md` (should be none), the list of `draft` items count by section, and one suggested next step, and the number of image slots with the 3 highest-priority ones to find first. No long recap