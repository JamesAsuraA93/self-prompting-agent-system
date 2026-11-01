# Task
Build a one-page static company profile site in Thai for Doi Phrao Hill Roasters, a fictional specialty coffee roaster that sells to cafes and offices in northern Thailand.
The result goes in the project folder as plain HTML, CSS and JavaScript, ready to drop on any static host.

## Why this matters
Cafe owners find suppliers through LINE groups and Google, then judge them in a few seconds on a phone.
The site has to load fast on a weak mobile connection, read naturally in Thai, and make it easy to get in touch.
The company is fictional; the site exists as a demo, so it must never claim anything that is not in the facts below.

## Context
Cafe owners and office managers in Chiang Mai, mostly on phones, some on laptops.
Plain HTML, CSS and JavaScript, no build step, no frameworks, no dependencies.
The project folder currently holds only `reqs.md`, so you are starting from an empty site.
The machine has Node 22, and Playwright with Chromium is installed globally: `require('playwright')` works from any directory and `chromium.launch()` needs no options.
You can use it to look at the page and check your work. Keep any helper scripts or packages outside the project folder (for example in /tmp), because the project must stay plain files with no tooling.

## What to deliver
`index.html`, `404.html`, `styles.css` and `main.js` at the root of the project folder, and nothing else that the site needs at runtime.

## Current state
The site already exists in the project folder and passes every acceptance criterion, including the [judgment] criterion AC15.
This run is a polish pass on notes from the last review. Keep everything that works and change only what this section asks for.

Fix these review notes, quoted from the reviewer:
1. "On desktop (>=900 px) the footer's fictional-company notice wraps onto a second line inside a box roughly 40% wider than the text, leaving a large empty area on the right."
2. "On mobile, the first service card breaks 'คั่วตามโปรไฟล์ / ที่ร้านเลือก ส่งทุกสัปดาห์', leaving a short first line. The nowrap spans force the early break. The same happens at 1024 px."
3. "At 360 px the two hero buttons stack with unequal widths, which looks slightly ragged. At 375 px they fit on one row."
4. "The hero repeats the company name that is already in the header."
5. "The brand link and the footer 'กลับขึ้นด้านบน' link use href="#top", but no element has id="top"."
6. "After a nav jump, the section top lands at 64 px while the header bottom is at 65 px, a 1 px overlap that cannot be seen." Fix it anyway so the section starts exactly below the header.

For note 4, every company fact must still appear on the page exactly as written, so if you remove or change the hero's name label, confirm the name still appears verbatim elsewhere.
AC13 was reworded to cover executable scripts only; no change to the site is needed for it.

## Lessons from earlier runs
- Thai line breaking: Chromium's dictionary splits some loanwords and compounds in the wrong place (ทุกล็อต, บาริสต้า, ลาเต้อาร์ต, บรรจุภัณฑ์). Keep such short phrases together with an inline `white-space: nowrap` span, never `display: inline-block`, which strands whole fragments on their own lines in narrow columns.
- Check the layout at 1024 px as well as 375 px and 1280 px: multi-column cards are at their narrowest there.

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

## When something is unclear
Make the reasonable choice and keep going.
List each assumption in your final report.

## Before you finish
Check your work against every acceptance criterion; for each one, report PASS or FAIL and how you checked it, running code against the real page where you can.
Look at the page yourself at 360 px, 375 px, 1024 px, 1280 px and 1440 px, in light and dark mode, paying particular attention to how Thai text wraps inside cards, and fix anything that looks unfinished.
