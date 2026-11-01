# Verdict

Hard criteria: 14 of 14 passed
Failed or unclear: none
Must-have requirements not met: none
House rules: PASS (`temper.py rules-check` on the four site files: "RULES=pass"; a separate scan for U+2014, U+2013, U+2015 and the spaced double hyphen found nothing)

Method: I served the site folder with `python3 -m http.server 8765`, drove it with Playwright Chromium and ran axe-core 4.10.2 (installed under /tmp). Scripts, outputs and screenshots are in /tmp/judge004. The page font on this machine resolved to Loma for Thai and DejaVu Sans Mono for numerals (checked with CDP `CSS.getPlatformFontsForNode`).

## AC1: R1 holds: the four files exist at the root, there are no other runtime files, and their total size is under 100 KB.
Verdict: PASS
Evidence: `du -cb index.html 404.html styles.css main.js` gives 29805 + 10627 + 35710 + 5272 = "81414 total". The only other files at the root are `reqs.md` and `rules.md`, which are project docs and not runtime files, plus the tool's `.temper/` folder. There is no package.json and no image or font file. styles.css has no `url()` references.

## AC2: Loading `index.html` and `404.html` from a local static server makes no request to any other host.
Verdict: PASS
Evidence: I logged every request while each page loaded and was scrolled to the bottom: `AC2 hosts index.html: ["127.0.0.1:8765"]`, `AC2 hosts 404.html: ["127.0.0.1:8765"]`, and the same for a missing path. The favicon is an inline `data:` SVG. `https://schema.org` appears only as a JSON-LD string and is never fetched.

## AC3: The seven sections exist in the R3 order with the R3 ids, and the header nav has a link to each of the six non-hero sections.
Verdict: PASS
Evidence: `section ids: ["hero","about","services","process","team","testimonials","contact"]`; `header nav hrefs: ["#about","#services","#process","#team","#testimonials","#contact"]`.

## AC4: `lang="th"`, one `h1`, and the first Tab press focuses a skip link whose target is the main content.
Verdict: PASS
Evidence: `lang: th`, `h1 count: 1`. After the first Tab: `{"tag":"A","cls":"skip-link","href":"#main","text":"ข้ามไปยังเนื้อหาหลัก","visible":[8,8,183,45]}`. `#main` is the `<main>` element. Pressing Enter on it gives `{"hash":"#main","active":"main"}`, so focus moves into main.

## AC5: Each fact from the Company facts list is present verbatim in the page text; the page contains no phone number or email address other than the facts; the footer has the fictional-company notice.
Verdict: PASS
Evidence: I checked 35 fact strings, covering the name in both languages, tagline, year, the full About sentence, the 4 services with their descriptions, the 4 process steps, the 4 team members with their roles, the 3 quotes with their sources, address, phone, email and hours. `missing (textContent): []` and `missing (innerText): []`. `emails in html: ["hello@doiphraohill.example"]`; `phone-like in text: ["053 000 4567"]`; `tel hrefs: ["tel:0530004567","tel:0530004567"]`, which is the same number. Footer: "ดอยพร้าวฮิลล์ โรสเตอร์ส เป็นบริษัทสมมติ เว็บไซต์นี้จัดทำขึ้นเพื่อการสาธิตเท่านั้น ข้อมูลทั้งหมดไม่ใช่ข้อมูลจริง".
Note: the quotes are shown with curly marks (“ ”) instead of the straight quotes used in reqs.md. The quoted text itself matches exactly.

## AC6: `scrollWidth` does not exceed the viewport width at 360, 768 and 1280 px.
Verdict: PASS
Evidence: For both pages in both themes, scrollWidth equals innerWidth at every width tested: `light 360 index.html: {"sw":360,"iw":360}`, `768: {"sw":768}`, `1280: {"sw":1280}`, and the same in dark mode. I also tested 320, 375, 1024 and 1440 with the same result.

## AC7: At 375 px the menu button starts with `aria-expanded="false"`, `aria-controls` names the nav element, a click and an Enter press each toggle it, and Escape closes it with focus returning to the button. At 1280 px the nav links are visible and the button is not.
Verdict: PASS
Evidence:
- Initial state: `{"exp":"false","controls":"site-nav","navTag":"NAV","btnVisible":true,"navVisible":false}`.
- Click: `"exp":"true"`, nav visible. A second click: `"false"`, nav hidden.
- Enter: `"true"`, then `"false"`. Space: `"true"`.
- Tab into the first link, then Escape: `{"exp":"false","navVisible":false,"focusIsBtn":true}`.
- Choosing a link closes the menu and goes to `#team`.
- `1280: {"btnVisible":false,"linksVisible":[true x6]}`. The breakpoint holds at the edge: 767 px shows the button with hidden links, and 768 px shows the links with no button.

## AC8: axe-core 4.10 reports zero violations on `index.html` in light and dark color schemes.
Verdict: PASS
Evidence: axe 4.10.2, `violations: []` on index.html at 375 and 1280 px in both light and dark. The only incomplete result is `color-contrast` (34 to 36 nodes), which comes from gradient or overlapping backgrounds and is not a violation. I spot-checked the main text pairs by hand and all pass AA:
- light muted on paper: 6.81
- light tag-muted on tag: 5.25
- dark muted on paper: 8.58
- dark h1 accent: 4.8 at display size
- white step numbers on their marker: 5.08

Extra runs also returned `[]` with the mobile menu open and with the form in its error state, in both themes, and on 404.html.

## AC9: The R10 metadata is present, the description length is 50 to 160 characters, and the JSON-LD values equal the facts.
Verdict: PASS
Evidence:
- title: "ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters) | กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ"
- `desc len: 110`
- og:title, og:description and og:type ("website") are all present.
- JSON-LD: `{"type":"Organization","name":"ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)","telephone":"053 000 4567","email":"hello@doiphraohill.example","address":"99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190"}`.

Note: the JSON-LD name joins the Thai and English names, as the facts list writes them. The address is a plain string, not a PostalAddress. Both match the facts literally.

## AC10: An empty submit shows a Thai error for each of the three fields with `aria-invalid="true"` and `aria-describedby` pointing at the message, and the page does not navigate. A valid submit navigates to a `mailto:hello@doiphraohill.example` URL whose subject decodes to `ติดต่อจากเว็บไซต์` and whose body contains the typed message.
Verdict: PASS
Evidence:
- Empty submit: all three fields have `invalid:"true"`, `describedby` set to `name-error`, `email-error` and `message-error`, a visible message in the same `.field`, and the texts "กรุณากรอกชื่อของคุณหรือชื่อร้าน", "กรุณากรอกอีเมล" and "กรุณากรอกข้อความที่ต้องการส่งถึงเรา".
- No navigation: a window marker survived (`42`), `navs so far: 0`, and focus went to `name`.
- Valid submit with a two-line message containing `& 100% ?`: the browser navigated to `mailto:hello@doiphraohill.example?subject=...&body=...`. Decoded: `subject: "ติดต่อจากเว็บไซต์"`, `bodyContains: true`. The body also includes the name and reply email after the message.

## AC11: There are no `<img>` elements and no image files, and each team member's initials are shown.
Verdict: PASS
Evidence: `img count: 0` (I also checked for picture, source and image elements). There are no image files on disk. Each member shows initials: "ปว | ปาริชาติ วงศ์คำ", "ธส | ธนกร แสนดี", "มจ | มยุรี ใจงาม", "สท | สมเกียรติ ทองมา". All icons are inline SVG.

## AC12: With reduced motion emulated, no element has a non-zero transition or animation duration.
Verdict: PASS
Evidence: I scanned every element and its ::before and ::after under `reducedMotion: 'reduce'`. index.html (with the menu open) gives `{"bad":[],"anims":0}`, and 404.html gives the same. After hovering a button and a nav link at 1280 px: `[[],0]`.

## AC13: Every executable `<script>` (anything except JSON-LD data blocks) has `defer` or `type="module"`.
Verdict: PASS
Evidence: `scripts: [{"type":"application/ld+json"},{"src":"main.js","defer":true}]`. 404.html has no scripts.

## AC14: `404.html` has `lang="th"`, uses `styles.css`, and links to `index.html`.
Verdict: PASS
Evidence: `{"lang":"th","css":["styles.css"],"links":["#main","index.html","index.html"],"h1":["ไม่พบหน้าที่คุณต้องการ"]}`.

## Must-have requirements, tested beyond the criteria
- R1 to R4, R10, R12, R14: covered above with no gaps.
- R5: there are no other emails anywhere in the HTML source, and 404.html has no contact data at all.
- R6: also holds at 320, 375, 1024 and 1440 px, in both themes, on both pages.
- R7: Space toggles the menu. Escape works from inside the nav as well as from the button. A click outside the header closes the menu, and so does crossing 768 px.
- R8: both themes are readable. The pairs I measured are listed under AC8.
- R9: holds on index.html in both themes, including the open-menu and form-error states.
- R11: inputs of my own:
  - name filled, email `abc@`, message of only spaces: name valid, email "รูปแบบอีเมลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง", message flagged. The trimming works.
  - `a@b` and `a b@c.d`: rejected.
  - `x@y.co` and `ก@ข.ค`: accepted.
  - After a valid submit, every `aria-invalid` is cleared and a fallback mailto link appears in the status region.
- R13: holds on both pages.
- R15: 404.html is in Thai and uses the same header, topo lines, ridge and footer. It links home twice.
- R16: met. See AC16.

No must-have failed.

## Advisory

AC15 [judgment]: PASS. At 375 and 1280 px, in both themes, there is no overlapping or clipped text. Thai lines break at phrase boundaries because of the `.kw` nowrap chunks. Body text is 17 px at a line-height of 1.75. The hierarchy is clear: an 80 px hero line, then 46 px h2, a 31 px statement, 20 px h3 and 17 px body. Vertical rhythm is steady at 64 px section padding on phones and 96 px from tablet up. Nits 1 to 6 and 14 to 16 below are polish items, not breakage.

AC16 [judgment]: PASS. The site is memorable.
- The palette comes from the subject: mist, coffee cherry, green bean, kraft, forest and dark roast.
- The type scale has strong contrast between the hero line and the small mono labels.
- Several signature elements are drawn in SVG and CSS: a kraft lot tag on a string carrying the founding year, shop count and phone; topographic contour lines; a hill-ridge skyline that ends the hero and starts the footer; the process drawn as a roast curve with charge and drop points; the team as cups of coffee seen from above on a cupping table; and a 404 whose zero is a cup.
- Every section has its own layout: a split hero, a two-column statement, a menu-board list, a dark chart band, the table of cups, an asymmetric quote layout and a contact list beside an order-slip form. Nothing repeats the card grid.

AC17 [judgment]: PASS, with reservations.
- One spacing scale (`--s-1` to `--s-9`) drives nearly all layout spacing. Raw px values appear only for illustration geometry and for the ridge allowances (+40 px, +32 px).
- Content edges line up on the container, and the hanging quote marks deliberately sit in the margin.
- Hover states match the style: a cherry underline grows under nav links, buttons darken and their arrows nudge, and ghost buttons turn cherry. Focus rings are forest green on light backgrounds and gold on dark bands.
- The dark theme is designed, not inverted. The tag and cups keep their real material colours, the table turns to dark wood, the red fill is deepened while line accents get brighter, and the footer ridge gets a kraft rim so it stays visible.
- The reservations are nits 7, 8 and 11 to 13.

Nits, numbered. None of these is a failure on its own.
1. Testimonials at 960 px and up: the lead quote runs only two lines, which leaves a large empty block under it in the left column while the right column holds two quotes. The composition feels bottom-light on the left.
2. Services at 1200 px and up: a full-width rule sits above the section, and the menu list's own top rule sits 48 px lower on the right half only. The two parallel rules at different offsets read as a doubled line.
3. Services at 1200 px and up: the kicker and heading on the left do not line up with the first row on the right. The kicker sits about 12 px below the first rule, and the first service name sits about 28 px lower again.
4. Hero at 360 to 1023 px: the contour lines run behind the lead paragraph and the h1, so thin green strokes cross the Thai text. They are low in contrast, but the text loses some crispness.
5. Testimonials at 375 and 768 px: the space below the last quote (quote padding plus section padding, about 96 to 130 px) is noticeably larger than the space above the heading.
6. Contact at 768 to 959 px: the form stretches to the full 704 px content width, which makes the inputs and the button very long. A max-width or an earlier two-column layout would sit better.
7. The open quote glyph “ in Loma Bold renders as two straight lowered ticks, unlike the slanted close glyph ”, so the pair looks mismatched at display size. This depends on the font; on macOS and Windows a different face would be used.
8. The phone number in the contact list is set in bold 26 px DejaVu Sans Mono beside Loma text. It works on the tag, where the typewriter feel fits, but in the contact list it looks heavier and more technical than everything around it.
9. Mobile menu: the button label stays "เมนู" when the menu is open. Only the icon changes to an X. A "ปิด" label would make the open state clearer.
10. 404 at 375 px: the cup handle almost touches the second "4" (a gap of about 10 px), while the first "4" has more room. At 1280 px the spacing is fine.
11. Dark theme: the cherry kicker dots (#b3293c on #111813, 2.8:1) nearly disappear. They are decorative, but they were a visible detail in light mode.
12. Dark theme: the hero h1 accent (#e85d6f) leans toward candy pink against the deep green mist. The comment in styles.css says the intent was to avoid exactly that, and it only partly succeeds at large sizes.
13. Process on mobile: the vertical track starts from a near-transparent gradient, so the connector between steps 1 and 2 is almost invisible.
14. Team on mobile: only the founder's role wraps to two lines ("ผู้ก่อตั้ง / และหัวหน้าโรงคั่ว"), so the two cards in the first row end at different heights.
15. Team at 768 px and up: each cup is centred, but its handle sticks out about 26 px to the right. The visual mass sits slightly right of the centred name below.
16. Footer: "(Doi Phrao Hill Roasters)" sits on its own line but keeps its parentheses, which only make sense inline.
17. Form error state at 1280 px: after the scroll to the first invalid field, the form title "ส่งข้อความถึงเรา" and the first line of the contact heading end up under the sticky header. The field label itself stays visible, which is what matters.
18. 404 page: the footer markup has an empty line where index.html has the footer ridge SVG. It causes no visual problem, since the 404 hero ridge runs into the footer instead, but it is a leftover.

## Other observations
- The build is clean: no console errors appeared during the runs, and there is no tooling in the folder.
- On this Linux test machine the whole site rendered in the fallback faces Loma and DejaVu Sans Mono. The font stack lists Sukhumvit Set, Thonburi and Leelawadee UI first, so the look will differ, probably for the better, on Apple and Windows devices, which is where most visitors will be.
- Requirements note: AC5 says "verbatim", while the facts list writes the quotes with straight marks. If the user wants the quote marks themselves to match, the requirements should say so. As written, the quoted text matches exactly.
