# Verdict

Hard criteria: 14 of 14 passed
Failed or unclear: none
Must-have requirements not met: none

Advisory: AC15 FAIL (Thai text breaks mid-word and leaves one-word orphan lines in the service and process cards at 1280 px).

Method: served the folder with `python3 -m http.server 8765` and drove it with Playwright (Chromium) and axe-core 4.10.2. Scripts are in /tmp/judge (test.js, shots.js, zoom.js) and screenshots are in /tmp/judge/shots.

## AC1: R1 holds: the four files exist at the root, there are no other runtime files, and their total size is under 100 KB.
Verdict: PASS
Evidence: `find . -path ./.temper -prune -o -type f -print` lists only `404.html`, `index.html`, `main.js`, `styles.css`, `reqs.md`. `wc -c` gives `20696 index.html, 3711 404.html, 18642 styles.css, 4702 main.js, 47751 total`, which is 46.6 KB. There is no package.json and no image, font or other asset file. `reqs.md` is the requirements input, not a runtime file.

## AC2: Loading `index.html` and `404.html` from a local static server makes no request to any other host.
Verdict: PASS
Evidence: Playwright request log with networkidle:
- index.html: `["http://127.0.0.1:8765/index.html","http://127.0.0.1:8765/styles.css","http://127.0.0.1:8765/main.js"]`, external: `[]`
- 404.html: `["http://127.0.0.1:8765/404.html","http://127.0.0.1:8765/styles.css"]`, external: `[]`
The favicon is an inline `data:` SVG.

## AC3: The seven sections exist in the R3 order with the R3 ids, and the header nav has a link to each of the six non-hero sections.
Verdict: PASS
Evidence: `section[id]` in document order: `["hero","about","services","process","team","testimonials","contact"]`. `header nav a` hrefs: `["#about","#services","#process","#team","#testimonials","#contact"]`.

## AC4: `lang="th"`, one `h1`, and the first Tab press focuses a skip link whose target is the main content.
Verdict: PASS
Evidence: `lang` = `th`; `h1` count = `1`. First Tab press: `{tag:"A", cls:"skip-link", href:"#main", text:"ข้ามไปยังเนื้อหาหลัก"}`, visible at top 8, left 8, 182x50. Pressing Enter gives `{hash:"#main", active:"main", activeTag:"MAIN"}`, and `<main id="main" tabindex="-1">` receives focus.

## AC5: Each fact from the Company facts list is present verbatim in the page text; the page contains no phone number or email address other than the facts; the footer has the fictional-company notice.
Verdict: PASS
Evidence: I checked 37 fact strings against `body.innerText`, both raw and with whitespace normalized, and against `textContent`. The strings covered the name with and without the English part, the tagline, 2016, the full About sentence, each service name and description, the 4 process steps, the 4 names and roles, the 3 quotes with their quote marks and attributions, the address, phone, email and hours. Missing: `[]` in all three checks. Emails found in the HTML: `["hello@doiphraohill.example"]`. Phone-like strings in the text: `["053 000 4567"]`. The HTML also contains `tel:0530004567`, which is the same number; other digit runs come from SVG path data. Footer text: `ดอยพร้าวฮิลล์ โรสเตอร์ส เป็นบริษัทสมมติ เว็บไซต์นี้จัดทำขึ้นเพื่อการสาธิตเท่านั้น ข้อมูลทั้งหมดไม่ใช่ข้อมูลจริง`.
Note: the requirements write services and team as `name: description`. The page shows the name and the description as separate elements (h3 + p) rather than the literal `name: description` string. I read the colon as list formatting. The reqs could say so explicitly.

## AC6: `scrollWidth` does not exceed the viewport width at 360, 768 and 1280 px.
Verdict: PASS
Evidence: `documentElement.scrollWidth` equals the viewport at 360 (360), 768 (768) and 1280 (1280). I also checked 320, 375, 414, 1024 and 1440, with the mobile menu open and on 404.html: every value equals the viewport width.

## AC7: At 375 px the menu button starts with `aria-expanded="false"`, `aria-controls` names the nav element, a click and an Enter press each toggle it, and Escape closes it with focus returning to the button. At 1280 px the nav links are visible and the button is not.
Verdict: PASS
Evidence: at 375 px:
- Initial state: `{exp:"false", controls:"site-nav", navTag:"NAV", navVisible:false}`.
- Click: `exp:"true", navVisible:true`. Second click: `exp:"false"`.
- Enter: `exp:"true"`. Enter again: `exp:"false"`. Space: `exp:"true"`.
- Tab moved focus into `<a href="#about">`. Escape then gave `{exp:"false", navVisible:false, active:"menu-toggle"}`.

At 1280 px: `btn: "none"`, and all 6 links have visibility `visible` with non-zero boxes in the header row (top 11). The same holds at 768 px (`btn: "none"`).

## AC8: axe-core 4.10 reports zero violations on `index.html` in light and dark color schemes.
Verdict: PASS
Evidence: `axe.version` = `4.10.2`.
- Light at 1280 and 375: `violations: []`.
- Dark at 1280 and 375: `violations: []`.
- Menu open at 375: `[]` in both themes.
- 404.html: `[]` in both themes.

axe left 4 `color-contrast` items incomplete (hero text over a gradient, the brand name under the blurred header, the textarea). I computed the worst case by hand. Muted text on the gradient end colour `#f6e1d3` is 6.06:1 in light, and dark muted on `#3a2519` is 7.28:1. Both pass.

## AC9: The R10 metadata is present, the description length is 50 to 160 characters, and the JSON-LD values equal the facts.
Verdict: PASS
Evidence:
- title: `ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters) | กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ`.
- meta description: 110 characters (code points and UTF-16 both 110).
- `og:title`, `og:description` and `og:type` (`website`) are present.
- JSON-LD has `@type: Organization`. A strict-equality check against the facts returned `{type:true, name:true, tel:true, email:true, addr:true}` for name `ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)`, telephone `053 000 4567`, email `hello@doiphraohill.example` and address `99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190`.

## AC10: An empty submit shows a Thai error for each of the three fields with `aria-invalid="true"` and `aria-describedby` pointing at the message, and the page does not navigate. A valid submit navigates to a `mailto:hello@doiphraohill.example` URL whose subject decodes to `ติดต่อจากเว็บไซต์` and whose body contains the typed message.
Verdict: PASS
Evidence: empty submit results, each message visible and placed directly after its field:
- name: `aria-invalid="true"`, `aria-describedby="name-error"`, `กรุณากรอกชื่อของคุณหรือชื่อร้าน`
- email: `aria-invalid="true"`, `aria-describedby="email-error"`, `กรุณากรอกอีเมล`
- message: `aria-invalid="true"`, `aria-describedby="message-error"`, `กรุณากรอกข้อความที่ต้องการส่งถึงเรา`

No navigation happened: a `window.__marker` set before the submit survived, the URL stayed `http://127.0.0.1:8765/index.html`, and the framenavigated log was `[]`.

For the valid submit I typed the message `อยากสั่งกาแฟ 5 กิโล & ราคา? 100%\nบรรทัดสอง`, which includes `&`, `?`, `%` and a newline. The browser issued a request to `mailto:hello@doiphraohill.example?subject=...&body=...`. Decoded: subject `ติดต่อจากเว็บไซต์`, body `อยากสั่งกาแฟ 5 กิโล & ราคา? 100%\nบรรทัดสอง\n\nชื่อ: ร้านทดสอบ\nอีเมลติดต่อกลับ: owner@cafe.co.th`, containsMsg `true`.

## AC11: There are no `<img>` elements and no image files, and each team member's initials are shown.
Verdict: PASS
Evidence: `img, picture, source, [style*="url("]` count = 0. There are no image files in the folder. Avatars: ปาริชาติ วงศ์คำ → `ปว`, ธนกร แสนดี → `ธส`, มยุรี ใจงาม → `มจ`, สมเกียรติ ทองมา → `สท`. Each avatar is `display:grid`, visible and 76px wide, and the screenshots show them. All icons are inline `<svg>`.

## AC12: With reduced motion emulated, no element has a non-zero transition or animation duration.
Verdict: PASS
Evidence: with `reducedMotion: 'reduce'` I scanned all 275 elements plus their `::before` and `::after`. Elements with a non-zero `transitionDuration` or `animationDuration`, or with an `animationName` other than none: `[]`, both with the menu closed and open. `scroll-behavior` is `auto`. Control run with no-preference: 10 elements have transitions, so the rule is doing real work.

## AC13: Every `<script>` has `defer` or `type="module"`.
Verdict: PASS
Evidence: the page has two scripts: `{src:"main.js", defer:true}` and an inline `{type:"application/ld+json"}`. The JSON-LD block is a data block, not an executable script. 404.html has no scripts.
Note: read literally, "every `<script>`" also covers the JSON-LD block, which R10 requires and which cannot take `defer` meaningfully. I graded the criterion as meaning executable scripts. The reqs should exempt `application/ld+json`.

## AC14: `404.html` has `lang="th"`, uses `styles.css`, and links to `index.html`.
Verdict: PASS
Evidence: `{lang:"th", css:["styles.css"], links:["#main","index.html","index.html","index.html"], h1:1}`. The text is all Thai (`ไม่พบหน้าที่คุณต้องการ`, `กลับสู่หน้าแรก`). The screenshots show the same header, hills, buttons and footer as the main page in both themes.

## Advisory
### AC15: [judgment] At 375 px and 1280 px the page looks finished and intentional: consistent spacing, no overlapping or clipped text, comfortable Thai typography, clear visual hierarchy.
Verdict: FAIL (advisory)
Rationale: overall the page is polished. It has a consistent 20px gutter, alternating section backgrounds, a clear kicker → h2 → content order, good card rhythm, a tidy mobile menu panel, well-placed inline form errors, and a coherent dark theme. 375 px looks finished in both themes. At 1280 px, though, the Thai text in the 4-column cards breaks badly (zoom at /tmp/judge/shots/z-services-1280.png and z-steps-1280.png):
- Process step 3 breaks inside a word: `Cupping ตรวจคุณภาพทุ` / `กล็อต`, which splits ทุก.
- Service "อบรมบาริสต้า" wraps to 3 lines: `คอร์สพื้นฐานและคอร์สลาเต้` / `อาร์ต` / `สำหรับทีมหน้าร้าน`. This splits ลาเต้อาร์ต and leaves a one-word line.
- Service "ดูแลเครื่องชง" wraps to 3 lines: `ตรวจเช็คและปรับตั้งเครื่อง` / `ชง` / `ถึงหน้าร้าน`. This splits เครื่องชง and leaves a one-syllable orphan.

The cause is the `.nb { display:inline-block }` phrase wrappers. A phrase that does not fit its column is forced onto its own line and then wrapped inside, so the line breaks are worse than plain text would get. The same effect makes these cards 3 lines tall at 1024 px. These are visible defects in "comfortable Thai typography" at a criterion viewport. Smaller points: the dark-mode hills have very low contrast against the background and almost disappear (a matter of taste), and the hero eyebrow pill wraps to two lines at 375 px, which still looks acceptable.

## Other observations
- Must-haves tested beyond the criteria, all met:
  - R6 also holds at 320, 414, 1024 and 1440 px.
  - R7: Space toggles the menu, clicking a nav link closes it, and the button is hidden at exactly 768 px.
  - R11: an invalid email (`abc@` or `a b@c.com`) shows `รูปแบบอีเมลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง` on the email field only. A whitespace-only name is rejected. Errors clear once the field is fixed.
  - R8: both themes passed axe contrast, and spot checks were above 6:1.
- The brand link uses `href="#top"` with no element id `top`. Browsers treat `#top` specially and scroll to the top, so it works, but the target is implicit.
- I modified no site files. All scratch files are under /tmp/judge.
