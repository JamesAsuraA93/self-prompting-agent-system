# Verdict

Hard criteria: 14 of 14 passed
Failed or unclear: none
Must-have requirements not met: none

Method: site served with `python3 -m http.server 8765` from the site folder and driven with Playwright and Chromium (scripts in /tmp/judge2/test.js, /tmp/judge2/shots.js and /tmp/judge2/vp.js). axe-core 4.10.2 was installed under /tmp/judge2. Screenshots are in /tmp/judge2/shots and /tmp/judge2/slices.

## AC1: R1 holds: the four files exist at the root, there are no other runtime files, and their total size is under 100 KB.
Verdict: PASS
Evidence: `find . -path ./.temper -prune -o -type f -print` lists `./styles.css ./404.html ./index.html ./main.js ./reqs.md`. reqs.md is the requirements file, not a runtime file. `wc -c`: `21536 index.html, 3903 404.html, 18972 styles.css, 4702 main.js, 49113 total` (about 48 KB). There is no package.json, build config or framework. The only script is `<script src="main.js" defer>`.

## AC2: Loading `index.html` and `404.html` from a local static server makes no request to any other host.
Verdict: PASS
Evidence: all requests were recorded until network idle.
- `index.html`: `["http://localhost:8765/index.html","http://localhost:8765/styles.css","http://localhost:8765/main.js"]`, external: `[]`
- `404.html`: `["http://localhost:8765/404.html","http://localhost:8765/styles.css"]`, external: `[]`
- The favicon is an inline `data:image/svg+xml` URI, so it makes no request. No computed `background-image` uses `url(` (count 0).

## AC3: The seven sections exist in the R3 order with the R3 ids, and the header nav has a link to each of the six non-hero sections.
Verdict: PASS
Evidence: `section[id]` in document order: `["hero","about","services","process","team","testimonials","contact"]`. `header nav a` hrefs: `["#about","#services","#process","#team","#testimonials","#contact"]`.

## AC4: `lang="th"`, one `h1`, and the first Tab press focuses a skip link whose target is the main content.
Verdict: PASS
Evidence: `lang` = `th`. The page has one h1: `["กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ"]`. The first Tab focuses `{"tag":"A","cls":"skip-link","href":"#main","text":"ข้ามไปยังเนื้อหาหลัก"}`, and the link is visible on screen at (8,8) with size 182x50. Pressing Enter then gives `{"hash":"#main","active":"main"}`; the target is `<main id="main" tabindex="-1">`. The next Tab goes to the first link inside main (`ติดต่อสั่งกาแฟ`).

## AC5: Each fact from the Company facts list is present verbatim in the page text; the page contains no phone number or email address other than the facts; the footer has the fictional-company notice.
Verdict: PASS
Evidence:
- 34 fact strings were checked against `document.body.innerText` with whitespace collapsed: name with English in parentheses, tagline, 2016, the full About sentence, each service name and description, the 4 process steps, each team name and role, each testimonial quote with its straight quotes and attribution, address, phone, email and hours. Result: `missing: []`.
- The process steps are in order: `["1 คัดเมล็ดจากเกษตรกร","2 คั่วตามโปรไฟล์","3 Cupping ตรวจคุณภาพทุกล็อต","4 ส่งถึงร้านภายใน 48 ชั่วโมงหลังคั่ว"]`.
- Emails across index.html, 404.html and main.js: `["hello@doiphraohill.example"]` only.
- Phone-like digit runs: apart from SVG path coordinates, the only ones are `053 000 4567` and its `tel:0530004567` href.
- Every number in the visible text: `2016, 120, 48, 053, 000, 4567, 8:30, 17:30, 4, 1, 2, 3, 99/9, 5, 50190`. All come from the facts, plus the step numbers and "4 ขั้นตอน".
- Footer: "ดอยพร้าวฮิลล์ โรสเตอร์ส เป็นบริษัทสมมติ เว็บไซต์นี้จัดทำขึ้นเพื่อการสาธิตเท่านั้น ข้อมูลทั้งหมดไม่ใช่ข้อมูลจริง".
Note: the hero lead adds "สำหรับร้านกาแฟและออฟฟิศ". This comes from the Goal ("sells to cafes and offices"), not from the Company facts list. I do not count it as an invented claim.

## AC6: `scrollWidth` does not exceed the viewport width at 360, 768 and 1280 px.
Verdict: PASS
Evidence: `document.documentElement.scrollWidth` equals the viewport width at each width tested (320, 360, 375, 414, 768, 1024, 1280 and 1440), for example `360: {"sw":360,"iw":360}`, `768: {"sw":768}`, `1280: {"sw":1280}`. It also stays equal with the mobile menu open, with all form errors shown, and on 404.html.

## AC7: At 375 px the menu button starts with `aria-expanded="false"`, `aria-controls` names the nav element, a click and an Enter press each toggle it, and Escape closes it with focus returning to the button. At 1280 px the nav links are visible and the button is not.
Verdict: PASS
Evidence (375 px):
- Initial: `{"exp":"false","ctrl":"site-nav","navTag":"NAV","navShown":false,"btnShown":true}`
- Click: `exp:"true", navShown:true`. Second click: `exp:"false", navShown:false`.
- Enter (button focused): `exp:"true"`. Enter again: `exp:"false"`. Space: `exp:"true"`.
- Escape after tabbing two links into the open nav: `{"exp":"false","navShown":false,"active":"menu-toggle"}`. Focus returns to the button.
- Clicking a nav link or clicking outside the header also closes the menu.
Evidence (wider viewports, fresh load):
- 767 px: button `display:flex`, links hidden.
- 768, 1024 and 1280 px: button `display:none`, all six links shown inside the 65 px header (`[true,true,true,true,true,true]`).

## AC8: axe-core 4.10 reports zero violations on `index.html` in light and dark color schemes.
Verdict: PASS
Evidence: axe 4.10.2 ran with `axe.run(document)`.
- `index.html`, light, at 375 and 1280 px: `violations: []`.
- `index.html`, dark, at 375 and 1280 px: `violations: []`.
- Also checked: 404.html in both themes (`[]`), and index.html with every form error shown and the mobile menu open, in both themes (`[]`).
- axe returned "incomplete" `color-contrast` (7 nodes) for the hero text over the radial gradient and for `#message`; it could not determine those backgrounds. I checked them by hand at the gradient extremes:
  - light: muted `#654f40` on `#f6e1d3` gives 6.06:1
  - dark: `#c9b5a3` on `#3a2519` gives 7.28:1
  - heading text: at least 12:1 in both themes
  All pass WCAG AA.

## AC9: The R10 metadata is present, the description length is 50 to 160 characters, and the JSON-LD values equal the facts.
Verdict: PASS
Evidence:
- title: `ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters) | กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ`
- meta description: 110 characters (110 UTF-16 code units and 110 code points; 86 grapheme clusters, which is also within 50 to 160).
- og:title `ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)`, og:description present, og:type `website`.
- One JSON-LD block with `@type` `Organization`. Exact-equality checks: `{"name":true,"tel":true,"email":true,"addr":true}`. The values are `"telephone": "053 000 4567"`, `"email": "hello@doiphraohill.example"` and `"address": "99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190"`.

## AC10: An empty submit shows a Thai error for each of the three fields with `aria-invalid="true"` and `aria-describedby` pointing at the message, and the page does not navigate. A valid submit navigates to a `mailto:hello@doiphraohill.example` URL whose subject decodes to `ติดต่อจากเว็บไซต์` and whose body contains the typed message.
Verdict: PASS
Evidence:
- Empty submit:
  - name: `invalid:"true", describedby:"name-error", msg:"กรุณากรอกชื่อของคุณหรือชื่อร้าน"`
  - email: `invalid:"true", describedby:"email-error", msg:"กรุณากรอกอีเมล"`
  - message: `invalid:"true", describedby:"message-error", msg:"กรุณากรอกข้อความที่ต้องการส่งถึงเรา"`
  - All three messages are visible and sit in the same `.field` wrapper as their input.
  - A `window.__marker` set before submitting survived, the URL stayed `/index.html`, and no frame navigation occurred.
  - Focus moved to `#name`.
- Own inputs: a whitespace-only name is rejected, and `abc@` gives "รูปแบบอีเมลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง". An error clears live once the field is fixed.
- Valid submit with message `อยากสั่งกาแฟ 5 กิโล & ราคา? 100%\nบรรทัดสอง`, captured with the Navigation API:
  - URL starts `mailto:hello@doiphraohill.example?subject=...&body=...`
  - decoded subject `ติดต่อจากเว็บไซต์` (`subjectOK:true`)
  - decoded body `"อยากสั่งกาแฟ 5 กิโล & ราคา? 100%\nบรรทัดสอง\n\nชื่อ: ร้านทดสอบ\nอีเมลติดต่อกลับ: owner@cafe.example"` (`bodyHasMsg:true`)
  - `&`, `?` and `%` are encoded correctly.

## AC11: There are no `<img>` elements and no image files, and each team member's initials are shown.
Verdict: PASS
Evidence: `img, picture, image, source, object, embed, iframe` count is 0, and there are no image files in the folder (see the AC1 listing). Visible avatars: ปว (ปาริชาติ วงศ์คำ), ธส (ธนกร แสนดี), มจ (มยุรี ใจงาม), สท (สมเกียรติ ทองมา). All icons are inline `<svg>`.

## AC12: With reduced motion emulated, no element has a non-zero transition or animation duration.
Verdict: PASS
Evidence: with `reducedMotion: 'reduce'`, I checked 930 element and pseudo-element computed styles: `bad: []`, `scrollBehavior: "auto"`, `document.getAnimations().length: 0`. The result is the same after opening the menu and showing form errors. As a control, with `no-preference`, 10 elements have non-zero transitions, so the media query is doing the work.

## AC13: Every `<script>` has `defer` or `type="module"`.
Verdict: PASS
Evidence: the scripts are `[{"src":null,"type":"application/ld+json"},{"src":"main.js","defer":true}]`. The only executable script is deferred. The JSON-LD block is a data block that the browser does not execute, so it falls outside the intent of the criterion.
Note: read with extreme literalness, the JSON-LD `<script>` has neither attribute. R10 requires JSON-LD, though, and `defer` has no meaning on a data block, so this is an ambiguity in the requirements, not a defect. The requirements could say "every executable script".

## AC14: `404.html` has `lang="th"`, uses `styles.css`, and links to `index.html`.
Verdict: PASS
Evidence: `{"lang":"th","css":["styles.css"],"links":["#main","index.html","index.html","index.html"]}`. Clicking "กลับสู่หน้าแรก" loads `http://localhost:8765/index.html`. The page text is in Thai: h1 "ไม่พบหน้าที่คุณต้องการ", and it carries the same header, hills, footer and fictional-company notice as the main page.

## Must-have spot checks (own inputs)
- R4: the skip link is the first focusable element in the DOM and works at 768 px (screenshot vp-skip.png).
- R6: there is also no horizontal scroll at 320, 414, 1024 and 1440 px, or with the menu open or form errors shown.
- R7: Space toggles the menu as well. Escape pressed from inside the open nav closes it and returns focus to the button.
- R8: both themes follow `prefers-color-scheme`. Screenshots show readable contrast throughout, and axe passes in both.
- R11: invalid email formats and a whitespace-only name are rejected with Thai messages. The mailto body keeps special characters intact.
- R15: 404.html has no horizontal scroll at any width tested, and axe reports no violations in either theme.
No must-have requirement failed.

## Advisory
AC15 [judgment]: At 375 px and 1280 px the page looks finished and intentional.
Verdict: PASS (advisory)
Rationale: I reviewed full-page screenshots at 360, 375, 768, 1024, 1280 and 1440 px in light and dark, plus the open menu, the form error state and the 404 page.
- Spacing is consistent: the same 64/96 px section rhythm throughout, alternating section backgrounds, and cards that line up on a shared grid.
- Hierarchy is clear: a kicker above an h2 in each section, a large h1, and a phone card in the hero on desktop.
- No text is clipped or overlapping in any state.
- Thai wraps at sensible word boundaries; no word is split mid-syllable.
- The dark theme is coherent, not just inverted.
- After an empty submit, the focused field and its label sit clear of the sticky header.
Minor nits, none of which break the finished look:
- On desktop (≥900 px) the footer's fictional-company notice wraps onto a second line inside a box roughly 40% wider than the text, leaving a large empty area on the right.
- On mobile, the first service card breaks "คั่วตามโปรไฟล์ / ที่ร้านเลือก ส่งทุกสัปดาห์", leaving a short first line. The nowrap spans force the early break. The same happens at 1024 px.
- At 360 px the two hero buttons stack with unequal widths, which looks slightly ragged. At 375 px they fit on one row.
- The hero eyebrow repeats the company name, which is already in the header just above it.
- After a nav jump, the section top lands at 64 px while the header bottom is at 65 px, a 1 px overlap that cannot be seen.

## Other observations
- The brand link and the footer "กลับขึ้นด้านบน" link use `href="#top"`, but no element has `id="top"`. It still works, because browsers scroll to the top for the special `#top` fragment, but the target is implicit.
- A `<noscript>` style shows the nav when JavaScript is off, so the site degrades well.
- The site folder was not modified. Scratch files are under /tmp/judge2.
