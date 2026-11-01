# Verdict

Hard criteria: 14 of 14 passed
Failed or unclear: none
Must-have requirements not met: none

Method: site served with `python3 -m http.server 8765` from the site folder; checks run with Playwright (Chromium) and axe-core 4.10.2 injected into the page. Scripts and screenshots are under /tmp/judge3.

## AC1: R1 holds: the four files exist at the root, there are no other runtime files, and their total size is under 100 KB.
Verdict: PASS
Evidence: `find . -path ./.temper -prune -o -type f -print` gives `./styles.css ./404.html ./index.html ./main.js ./reqs.md`. `wc -c` gives `21678 index.html, 4003 404.html, 20225 styles.css, 4702 main.js, 50608 total` (about 49.4 KB). There is no package.json and no build tooling. `reqs.md` is the requirements file, not a runtime file.

## AC2: Loading `index.html` and `404.html` from a local static server makes no request to any other host.
Verdict: PASS
Evidence: I loaded each page in light and dark at 375 px, scrolled to the bottom and resized to 1280 px. Every request went to localhost: index.html made `["http://localhost:8765/index.html","http://localhost:8765/styles.css","http://localhost:8765/main.js"]` and 404.html made `["http://localhost:8765/404.html","http://localhost:8765/styles.css"]`. The filtered list of other hosts was `[]` in all four runs. The only `http(s)://` strings in the source are the SVG xmlns inside a `data:` favicon and the JSON-LD `@context`, and neither one makes a request.

## AC3: The seven sections exist in the R3 order with the R3 ids, and the header nav has a link to each of the six non-hero sections.
Verdict: PASS
Evidence: `section[id]` in document order is `["hero","about","services","process","team","testimonials","contact"]`. The `header nav a` hrefs are `["#about","#services","#process","#team","#testimonials","#contact"]`.

## AC4: `lang="th"`, one `h1`, and the first Tab press focuses a skip link whose target is the main content.
Verdict: PASS
Evidence: `{"lang":"th","h1":1,"h1text":"กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ"}`. The first Tab focuses `{"cls":"skip-link","href":"#main","text":"ข้ามไปยังเนื้อหาหลัก","visibleTop":8}`, so the link is visible on screen when focused. Pressing Enter gives `{"active":"main","tag":"MAIN","hash":"#main"}`. `<main id="main" tabindex="-1">` receives focus. 404.html also puts the skip link first.

## AC5: Each fact from the Company facts list is present verbatim in the page text; the page contains no phone number or email address other than the facts; the footer has the fictional-company notice.
Verdict: PASS
Evidence:
- I checked 34 fact strings against `document.body.innerText`: the full name with the English in parentheses, the tagline, 2016, the full About sentence, every service name and its description, all 4 process steps, every team name and role, every testimonial quote and who said it, the address, the phone number, the email and the hours. Missing: `[]`.
- I scanned every attribute value and the whole outerHTML for email addresses. The only one found is `["hello@doiphraohill.example"]`.
- The tel and mailto hrefs are `["tel:0530004567","tel:0530004567","mailto:hello@doiphraohill.example"]`. `tel:0530004567` is the same number without spaces. The other digit runs the scan found are SVG path data, plus "30 - 17" from the business hours.
- The footer text reads: "ดอยพร้าวฮิลล์ โรสเตอร์ส เป็นบริษัทสมมติ เว็บไซต์นี้จัดทำขึ้นเพื่อการสาธิตเท่านั้น ข้อมูลทั้งหมดไม่ใช่ข้อมูลจริง".
- I found no invented claims. The extra copy only rephrases the facts ("สำหรับร้านกาแฟและออฟฟิศ" comes from the Goal; "กว่า 120 ร้าน" and "48 ชั่วโมง" are facts).

## AC6: `scrollWidth` does not exceed the viewport width at 360, 768 and 1280 px.
Verdict: PASS
Evidence: index.html gives `360 → sw 360`, `768 → sw 768` and `1280 → sw 1280`. I also tested 320, 375, 414, 600, 900, 1024 and 1440 on both index.html and 404.html. In every case scrollWidth equals the viewport width.

## AC7: At 375 px the menu button starts with `aria-expanded="false"`, `aria-controls` names the nav element, a click and an Enter press each toggle it, and Escape closes it with focus returning to the button. At 1280 px the nav links are visible and the button is not.
Verdict: PASS
Evidence:
- Initial state: `{"exp":"false","controls":"site-nav","navTag":"NAV","navShown":false}`.
- Click 1 gives `exp:"true", navShown:true` and click 2 gives `exp:"false", navShown:false`. Enter toggles true then false. Space toggles true then false.
- With the menu open, I tabbed into the nav (focus on "บริการ") and pressed Escape: `{"exp":"false","navShown":false,"focus":"menu-toggle"}`.
- Breakpoint: at 767 px it is `{"btn":"flex","nav":"none"}`; at 768 px it is `{"btn":"none","nav":"block"}` and all six links sit on one row with no overlap (brand 20-236, links 277-748).
- At 1280 px: `{"btn":"none","btnW":0}` and all six links are visible.
- Extras: clicking a nav link closes the menu, and the target section lands right under the sticky header (team top 64.98 px, header 65 px). Clicking outside the header also closes it.

## AC8: axe-core 4.10 reports zero violations on `index.html` in light and dark color schemes.
Verdict: PASS
Evidence:
- At 1280 px, light gives `{"version":"4.10.2","violations":[],"passes":42,"incomplete":["color-contrast:9"]}` and dark gives the same with `violations: []`.
- I also ran zero-violation passes at 375 px, at 375 px with the menu open, after an empty form submit, and on 404.html, each in both themes.
- The 9 incomplete items come from the hero gradient background and the textarea. I checked them by hand at the worst gradient stop. Light: muted #654f40 on #f6e1d3 = 6.06:1. Dark: #c9b5a3 on #3a2519 = 7.28:1. The dark h1 #f3e9dd on #3a2519 = 12.0:1. All pass AA.

## AC9: The R10 metadata is present, the description length is 50 to 160 characters, and the JSON-LD values equal the facts.
Verdict: PASS
Evidence:
- `title`: "ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters) | กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ".
- The description is 110 characters (both code points and UTF-16 length): "โรงคั่วกาแฟพิเศษในอำเภอพร้าว เชียงใหม่ คั่วตามโปรไฟล์ที่ร้านเลือก ส่งกาแฟคั่วสดถึงร้านภายใน 48 ชั่วโมงหลังคั่ว".
- `og:title`, `og:description` and `og:type="website"` are all present.
- The JSON-LD has one block, `@type: "Organization"`, with these values:
  - `name: "ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)"`
  - `telephone: "053 000 4567"`
  - `email: "hello@doiphraohill.example"`
  - `address: "99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190"`
- All four match the facts character for character.

Note (the requirement is ambiguous): R10 does not say whether `name` should be the full fact string including "(Doi Phrao Hill Roasters)" or only the Thai name, or whether `address` may or should be a structured PostalAddress. The output uses the literal fact strings, which is the strictest reading of "match the facts exactly". If a PostalAddress was intended, the requirement should say so.

## AC10: An empty submit shows a Thai error for each of the three fields with `aria-invalid="true"` and `aria-describedby` pointing at the message, and the page does not navigate. A valid submit navigates to a `mailto:hello@doiphraohill.example` URL whose subject decodes to `ติดต่อจากเว็บไซต์` and whose body contains the typed message.
Verdict: PASS
Evidence:
- Empty submit: every field gets `invalid:"true"` and a visible message placed directly after its field.
  - name: describedby "name-error", "กรุณากรอกชื่อของคุณหรือชื่อร้าน"
  - email: describedby "email-error", "กรุณากรอกอีเมล"
  - message: describedby "message-error", "กรุณากรอกข้อความที่ต้องการส่งถึงเรา"
- After the empty submit the page did not navigate (`navs: []`, the URL is unchanged) and focus moved to `#name`.
- Bad emails are rejected: `a b@c.de`, `abc@def`, `abc`, `@x.com` and `abc@x.` all get aria-invalid "true", and `test@example.com` clears it. A message of only spaces is rejected.
- Valid submit: the browser requested `mailto:hello@doiphraohill.example?subject=...&body=...`. Decoded, the subject is "ติดต่อจากเว็บไซต์" and the body is "สวัสดีครับ อยากสั่งกาแฟ 5 กิโล\nบรรทัดสอง & ? = # 100%\n\nชื่อ: ร้านทดสอบ & Co\nอีเมลติดต่อกลับ: test@example.com". The body contains the typed message, including a newline and the reserved characters `& ? = # %`.
- A fallback status link ("คลิกที่นี่เพื่อส่งอีเมล") is shown as well.

## AC11: There are no `<img>` elements and no image files, and each team member's initials are shown.
Verdict: PASS
Evidence: `img: 0`, and no `picture/object/embed/iframe/video` elements. No CSS rule uses `url()`. The folder has no image files. The four 76 px avatars are `["ปว","ปาริชาติ วงศ์คำ"], ["ธส","ธนกร แสนดี"], ["มจ","มยุรี ใจงาม"], ["สท","สมเกียรติ ทองมา"]`. All other icons are inline `<svg>`.
Note: the favicon is a `data:image/svg+xml` URI in a `<link rel="icon">`. It is not an image file and not an `<img>`, but strictly it is not "inline SVG" in the DOM either. I count it as compliant. If favicons should be excluded or required, the requirement should say which.

## AC12: With reduced motion emulated, no element has a non-zero transition or animation duration.
Verdict: PASS
Evidence: With `reducedMotion: 'reduce'` I checked every element plus its ::before and ::after: 936 element and pseudo combinations on index.html with the menu closed, again with the menu open, and 156 on 404.html. Result: `bad: []` in every case, and `scroll-behavior: auto`. Control: without reduce, 10 elements have non-zero transitions, which shows the override is what turns them off.

## AC13: Every executable `<script>` (anything except JSON-LD data blocks) has `defer` or `type="module"`.
Verdict: PASS
Evidence: The scripts are `[{"type":"application/ld+json"}, {"src":"main.js","defer":true}]`. 404.html has no scripts.

## AC14: `404.html` has `lang="th"`, uses `styles.css`, and links to `index.html`.
Verdict: PASS
Evidence: `{"lang":"th","css":["styles.css"]}`. Three links point to `index.html`: the brand, the "กลับสู่หน้าแรก" button and the footer link. All of the text is in Thai, and the page reuses the main site's header, hero gradient, hills and footer (seen in the screenshots).

## Advisory
### AC15 [judgment]: At 375 px and 1280 px the page looks finished and intentional: consistent spacing, no overlapping or clipped text, comfortable Thai typography, clear visual hierarchy.
Verdict: PASS (advisory)
Rationale: I took full-page screenshots at 360, 375, 768, 1024, 1280 and 1440 px in light and dark, plus the open menu, the form error state and the 404 page, and looked at all of them. The page looks like a coherent, finished company site:
- Warm coffee palette with clear section rhythm: kicker, then h2, then content, with 64/96 px section padding.
- Cards line up on one grid, and testimonial captions sit on a shared baseline.
- Generous Thai line-height (1.75), and `.kw` nowrap spans keep Thai compounds from breaking badly.
- A DOM check found no clipped or overflowing children in any card, step, stat, fact card or footer note at 360, 375, 1024, 1280 or 1440 px.
- Dark mode is properly re-tokenised, not inverted.

Nits I saw (none of them is a failure on its own):
1. Testimonials use straight ASCII `"..."` quotes right under a large decorative quote glyph. The quoting is doubled and the straight quotes look unfinished next to the styled glyph. Typographic “ ” quotes, or dropping the literal quotes, would look better.
2. Dark mode loses most of its structure. The alternating section bands (#1b1410 against #15100c), the footer (#0c0907) and the hero hills are nearly the same colour, so the sections run together. Light mode separates them clearly.
3. At 360/375 px the hero lead leaves "และออฟฟิศ" alone on a third line.
4. At 375 px two headings break with a short first line: "จากดอยถึง / ร้านคุณใน 4 ขั้นตอน" and "คุยกับเรา / เรื่องกาแฟของร้านคุณ". The balance is top-light, though the breaks fall at word boundaries.
5. On mobile, the service descriptions wrap at about 60-70% of the card width (for example "คั่วตามโปรไฟล์ที่ร้านเลือก / ส่งทุกสัปดาห์" and "ตรวจเช็คและปรับตั้ง / เครื่องชงถึงหน้าร้าน"), which leaves a lot of empty space on the right of each card. This is deliberate clause-breaking but looks ragged.
6. At 1024 px the About paragraph breaks "รับซื้อเมล็ด / ตรงจาก…", splitting the phrase "รับซื้อเมล็ดตรง" across lines.
7. At 1280 px the contact h2 wraps to "คุยกับเราเรื่องกาแฟ / ของร้านคุณ", and the left contact column ends far above the form, leaving a large empty block under the contact list.
8. On desktop, process steps 1 and 2 (one line of text) and testimonials 1 and 3 (two lines, next to a three-line middle quote) have visible empty space at the bottom of their equal-height cards.
9. At 1280 px the hero-stat labels are 13 px ("ปีที่ก่อตั้ง", "ร้านกาแฟที่เราส่งให้"). That is small for Thai with stacked tone marks next to 24 px numbers.
10. The footer's "กลับขึ้นด้านบน" link is vertically centred against the two-line brand block, so it sits about 12 px below the brand name's baseline instead of lining up with it.
11. On mobile, the open menu panel uses the page background with a shadow that disappears in dark mode, so the panel blends into the hero. Only the 1 px bottom border separates it. The links have no dividers.
12. On the 404 page, "กลับสู่หน้าแรก" appears twice (the button and the footer link). The page is also about 47 px taller than a 1280×1000 viewport even though the content is short, so it always scrolls a little.
13. The favicon (a coffee bean on a rust square) does not match the header brand mark (mountains and sun).
14. At 768-959 px the hero has no side card, so the right half of the hero is empty under the gradient. This is acceptable but looks a little sparse.

## Other observations
- All must-haves R1-R15 hold under my own extra inputs: more viewports (320-1440 px), Space-key toggling, outside-click and link-click menu closing, malformed emails, whitespace-only messages, reserved characters in the mailto body, and axe runs in the error, menu-open and 404 states. I found no must-have broken.
- The page works without JS: a `<noscript>` style shows the nav and hides the toggle.
- No files in the site were modified. All scratch files are in /tmp/judge3. I found an older /tmp/judge folder from an earlier run and did not use its scripts.
