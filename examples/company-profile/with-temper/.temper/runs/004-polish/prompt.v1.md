# Task
Polish the existing one-page Thai company profile site for Doi Phrao Hill Roasters until the last reviewer's notes are all resolved.
The site is plain HTML, CSS and JavaScript in the project folder and must stay that way.

## Why this matters
Cafe owners find suppliers through LINE groups and Google, then judge them in a few seconds on a phone.
The site has to load fast on a weak mobile connection, read naturally in Thai, and make it easy to get in touch.
The company is fictional; the site exists as a demo, so it must never claim anything that is not in the facts below.
The owner looked at the current site and felt it could be any company's template: tidy, but forgettable.
For a small roaster that sells on craft, the site itself has to show craft.

## Current state
The site passes every acceptance criterion, including the judgment criteria AC15, AC16 and AC17, after a redesign that gave it its own identity (contour map, kraft lot tag, roast curve, espresso cups).
Keep that identity and everything that works. This run fixes the reviewer's nits, quoted in full below with their numbers.

1. Copy repeats itself. The hero eyebrow, the about h2 ("โรงคั่วกาแฟพิเศษ จากอำเภอพร้าว") and the first line of the about paragraph ("โรงคั่วกาแฟพิเศษในอำเภอพร้าว") all say the same thing. The ledger beside it repeats the paragraph's facts ("อำเภอพร้าว จังหวัดเชียงใหม่", "ร้านกาแฟกว่า 120 ร้าน"), and 2016/120/48 also appear on the hero tag.
2. Contact at 960 px and up: the empty gap described under AC15, with `margin-top:auto` on `.contact-list`.
3. Dark theme: the footer ridge is roast #2a1c12 against contact #18231c, a ratio of 1.02:1. The hill silhouette that tops the footer effectively disappears.
4. Dark theme: the form card surface #1b251e against #18231c is 1.03:1. The order-slip card shows only through its 1 px border.
5. Dark theme: the cherry becomes a candy pink (#f08494). The pink primary buttons are the loudest thing on the page and lose the ripe-cherry and roast feel.
6. Dark theme: the focus ring (#f08494) and the error colour (#ff9d92) are nearly the same, so a focused invalid field barely differs from an unfocused one.
7. After an empty submit, focus jumps to `#name` but its label sits partly under the sticky header: label top at 54 px against header bottom at 65 px on mobile, 63 against 65 at 1280. `scroll-padding-top` covers the input but not the label.
8. The cup's porcelain ring (box-shadow 10 px, margin-left 8 px) sticks out about 2 px left of the name and role text edge.
9. Only the lead testimonial uses a hanging open quote. The two smaller quotes don't hang, which is inconsistent.
10. 404 page: the big "404" uses the system monospace, which draws a dotted zero, and its left edge sits a few px right of the h1 and body text edge (about 96 px against 89 to 92 px at 1280).
11. The roast curve starts with a sharp drop clipped at the container's left edge and runs off the right edge with no end. The dashed drop lines from markers to labels (14% alpha) are almost invisible.
12. Process labels at desktop are ragged: steps 1 and 2 take one line, steps 3 and 4 take two.
13. Team at desktop is the least composed section: four 84 px cups in a 1100 px row with a lot of empty space.
14. From 768 to 959 px the header is cramped: nav padding drops to 5 px, the brand subtitle is hidden, and the items almost touch.
15. At 1024 px and up there are about 190 px of empty space with one hairline between about and services.
16. Latin words ("Private Label", "Cupping", the email) render in a different system sans from the Thai, which causes a visible weight and size shift in "กาแฟ Private Label". This is expected without web fonts but noticeable.
17. On mobile the hero is about 1000 px tall because the tag stacks under the CTAs. Fine, but the tag dominates the first scroll.
18. Dead markup: `<circle class="topo-peak">` is `display:none` at every width.
19. Typography depends on the visitor having a Thai system font (Noto Sans Thai, Sukhumvit, Leelawadee and so on). Only the Chromium/Linux rendering was checked here.

Notes on specific items:
- Nit 1: trim the repetition with wording drawn only from the company facts; every fact must still appear verbatim somewhere on the page (AC5).
- Nit 16: web fonts and font files are ruled out by R1 and R2, but `@font-face` with `src: local(...)` and `unicode-range` loads nothing from the network and may be used to match Latin glyphs to the Thai font's size and weight. Do what you can within that and leave it if it cannot be improved cleanly.
- Nit 17: improve the first mobile scroll if you can do so without hiding the tag's facts.
- Nit 19 cannot be fixed without web fonts. Leave it and mention it in your report.

## Context
Cafe owners and office managers in Chiang Mai, mostly on phones, some on laptops.
Plain HTML, CSS and JavaScript, no build step, no frameworks, no dependencies.
The machine has Node 22, and Playwright with Chromium is installed globally: `require('playwright')` works from any directory and `chromium.launch()` needs no options.
Use it to look at the page and check your work. Keep helper scripts and packages outside the project folder (for example in /tmp).
A design skill is available through the Skill tool as `anthropic-skills:frontend-design`. Load it if it helps with any of the visual nits.
Fonts: R1 and R2 rule out web fonts, so the page uses the system Thai font stack. Identity has to come from composition, color, scale, inline SVG illustration and detail.

## What to deliver
The same four files at the root of the project folder: `index.html`, `404.html`, `styles.css`, `main.js`, and nothing else that the site needs at runtime.

## Company facts
Use these exactly. Do not invent other numbers, awards, clients or claims.

- Name: ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)
- Tagline: กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ
- Founded: 2016
- About: โรงคั่วกาแฟพิเศษในอำเภอพร้าว จังหวัดเชียงใหม่ รับซื้อเมล็ดตรงจากเกษตรกรบนดอย และส่งกาแฟคั่วสดให้ร้านกาแฟกว่า 120 ร้าน
- Services:
  - คั่วกาแฟสำหรับร้าน: คั่วตามโปรไฟล์ที่ร้านเลือก ส่งทุกสัปดาห์
  - กาแฟ Private Label: กาแฟคั่วพร้อมบรรจุภัณฑ์ในแบรนด์ของคุณเอง
  - อบรมบาริสต้า: คอร์สพื้นฐานและคอร์สลาเต้อาร์ตสำหรับทีมหน้าร้าน
  - ดูแลเครื่องชง: ตรวจเช็คและปรับตั้งเครื่องชงถึงหน้าร้าน
- Process (4 steps, in order):
  1. คัดเมล็ดจากเกษตรกร
  2. คั่วตามโปรไฟล์
  3. Cupping ตรวจคุณภาพทุกล็อต
  4. ส่งถึงร้านภายใน 48 ชั่วโมงหลังคั่ว
- Team:
  - ปาริชาติ วงศ์คำ: ผู้ก่อตั้งและหัวหน้าโรงคั่ว
  - ธนกร แสนดี: Q Grader
  - มยุรี ใจงาม: หัวหน้าฝ่ายอบรม
  - สมเกียรติ ทองมา: ฝ่ายดูแลลูกค้า
- Testimonials (quote: who):
  - "เมล็ดสดทุกล็อต ลูกค้าประจำสังเกตได้เลยว่ารสชาติคงที่ขึ้น": ร้านบ้านไม้ คาเฟ่
  - "ทีมอบรมใจเย็นมาก บาริสต้าใหม่ของเราชงได้มาตรฐานภายในสองสัปดาห์": ร้านลมหนาว
  - "สั่งวันจันทร์ ได้ของวันพุธ ไม่เคยพลาดสักครั้ง": ออฟฟิศสวนสัก
- Address: 99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190
- Phone: 053 000 4567
- Email: hello@doiphraohill.example
- Hours: จันทร์ - เสาร์ 8:30 - 17:30

## Requirements
- R1: Files at the project root: `index.html`, `404.html`, `styles.css`, `main.js`. No build step, no frameworks, no other runtime files. Total size of these files under 100 KB.
- R2: No network request leaves the host: no CDN, no web fonts from other domains, no analytics, no external images.
- R3: `index.html` has these sections in this order, with these ids: `hero`, `about`, `services`, `process`, `team`, `testimonials`, `contact`. The header navigation links to every section except `hero`.
- R4: `<html lang="th">`, exactly one `h1`, and a skip link that is the first focusable element and jumps to the main content.
- R5: Every company fact above appears on the page as written. No other phone numbers or email addresses appear. The footer says in Thai that the company is fictional and the site is a demo.
- R6: No horizontal scrolling at viewport widths 360, 768 and 1280 px.
- R7: Below 768 px the navigation collapses behind a menu button that has `aria-expanded` and `aria-controls`. Clicking it or pressing Enter or Space toggles the menu; Escape closes it and moves focus back to the button. At 768 px and wider the links are shown directly and the button is hidden.
- R8: Light and dark themes following `prefers-color-scheme`, both readable.
- R9: Accessibility: axe-core reports no violations on `index.html`, in both themes.
- R10: `<title>` contains the company name; a meta description between 50 and 160 characters; `og:title`, `og:description` and `og:type`; and JSON-LD of type Organization whose name, telephone, email and address match the facts exactly.
- R11: A contact form with name, email and message, all required. Submitting with missing or invalid fields shows a Thai error message next to each bad field, sets `aria-invalid="true"` on it, and links the message with `aria-describedby`, without reloading the page. A valid submit opens `mailto:hello@doiphraohill.example` with the subject `ติดต่อจากเว็บไซต์` and the message in the body.
- R12: No `<img>` elements and no image files. Team members are shown with their initials. Icons, if any, are inline SVG.
- R13: With `prefers-reduced-motion: reduce`, nothing animates or transitions.
- R14: Every script tag uses `defer` or `type="module"`.
- R15: `404.html` is in Thai, matches the main site's look, and links back to `index.html`.
- R16: The site has a design identity of its own that fits a small specialty roaster in the hills of Chiang Mai, not a generic landing-page template. Added after the first result, because the owner felt it looked like every other template. Taste has to come from composition, color, illustration and detail, since R1 and R2 rule out web fonts and image files.

## Constraints and out of scope
Plain HTML, CSS and JavaScript only.
Work in this folder; do not add a package.json or any tooling to the project.
Out of scope: A backend, a CMS, analytics, cookie banners, English translation, and deployment.

## Acceptance criteria
- AC1: R1 holds: the four files exist at the root, there are no other runtime files, and their total size is under 100 KB.
- AC2: Loading `index.html` and `404.html` from a local static server makes no request to any other host.
- AC3: The seven sections exist in the R3 order with the R3 ids, and the header nav has a link to each of the six non-hero sections.
- AC4: `lang="th"`, one `h1`, and the first Tab press focuses a skip link whose target is the main content.
- AC5: Each fact from the Company facts list is present verbatim in the page text; the page contains no phone number or email address other than the facts; the footer has the fictional-company notice.
- AC6: `scrollWidth` does not exceed the viewport width at 360, 768 and 1280 px.
- AC7: At 375 px the menu button starts with `aria-expanded="false"`, `aria-controls` names the nav element, a click and an Enter press each toggle it, and Escape closes it with focus returning to the button. At 1280 px the nav links are visible and the button is not.
- AC8: axe-core 4.10 reports zero violations on `index.html` in light and dark color schemes.
- AC9: The R10 metadata is present, the description length is 50 to 160 characters, and the JSON-LD values equal the facts.
- AC10: An empty submit shows a Thai error for each of the three fields with `aria-invalid="true"` and `aria-describedby` pointing at the message, and the page does not navigate. A valid submit navigates to a `mailto:hello@doiphraohill.example` URL whose subject decodes to `ติดต่อจากเว็บไซต์` and whose body contains the typed message.
- AC11: There are no `<img>` elements and no image files, and each team member's initials are shown.
- AC12: With reduced motion emulated, no element has a non-zero transition or animation duration.
- AC13: Every executable `<script>` (anything except JSON-LD data blocks) has `defer` or `type="module"`.
- AC14: `404.html` has `lang="th"`, uses `styles.css`, and links to `index.html`.
- AC15: [judgment] At 375 px and 1280 px the page looks finished and intentional: consistent spacing, no overlapping or clipped text, comfortable Thai typography, clear visual hierarchy.
- AC16: [judgment] A visitor would remember the site: a palette drawn from the subject, a type scale with real contrast, at least one distinctive visual element made in inline SVG or CSS, and sections whose layouts differ from each other instead of repeating one card grid.
- AC17: [judgment] The details feel crafted in both themes: one spacing scale used consistently, edges that line up, hover and focus states that match the style, and a dark theme that is designed rather than inverted.

## Lessons from earlier runs
- Thai line breaking: Chromium's dictionary splits some loanwords and compounds in the wrong place (ทุกล็อต, บาริสต้า, ลาเต้อาร์ต, บรรจุภัณฑ์). Keep such short phrases together with an inline `white-space: nowrap` span, never `display: inline-block`, which strands whole fragments on their own lines in narrow columns. (run 001, v1 to v2)
- Check the layout at 1024 px as well as 375 px and 1280 px: multi-column cards are at their narrowest there, and that is where the v1 wrapping problems showed. (run 001)
- Taste only shows up when reqs.md asks for it. The first two runs passed "looks finished" with a forgettable template; stating a design identity as `[judgment]` criteria (R16, AC16, AC17) is what moved it. (run 003-design)
- In dark mode, check decorative outlines and card edges against their own background, not only text contrast: the judge measured the footer hill outline and the form card edge at 1.02:1 and 1.03:1, which axe does not flag. (run 003-design)
- After a failed form submit, give fields a `scroll-margin-top` equal to the sticky header height, or the focused field's label lands under the header. (run 003-design)

## When something is unclear
Make the reasonable choice and keep going.
List each assumption in your final report.

## Before you finish
Check your work against every acceptance criterion; for each one, report PASS or FAIL and how you checked it, running code against the real page where you can.
Look at the page yourself at 360, 375, 768, 1024, 1280 and 1440 px, in light and dark mode, including the open menu, the form error state and the 404 page, and fix anything that looks unfinished.
