# Verdict

Hard criteria: 14 of 14 passed
Failed or unclear: none
Must-have requirements not met: none

Method: site served with `python3 -m http.server 8765` from the site folder; checks run with Playwright/Chromium (scripts and screenshots in /tmp/judge003). axe-core 4.10.2 installed under /tmp/judge003. Server stopped afterwards. No site file was modified.

## AC1: R1 holds: the four files exist at the root, there are no other runtime files, and their total size is under 100 KB.
Verdict: PASS
Evidence: `wc -c index.html 404.html styles.css main.js` -> `30312 index.html / 10746 404.html / 29834 styles.css / 4702 main.js / 75594 total` (73.8 KiB). Other files at the root: only `reqs.md` (the spec) and the `.temper` folder; no package.json, no other HTML/CSS/JS, `find ... -iname '*.png|*.jpg|*.svg|*.ico|...'` -> `0`.

## AC2: Loading `index.html` and `404.html` from a local static server makes no request to any other host.
Verdict: PASS
Evidence: every request logged, in light and dark, after scrolling to the bottom:
`index.html: [".../index.html", ".../styles.css", ".../main.js"], external: []`
`404.html: [".../404.html", ".../styles.css"], external: []`
The only `http(s)://` strings in the source are the SVG namespace inside a data: favicon and the JSON-LD `@context`, neither of which is fetched.

## AC3: The seven sections exist in the R3 order with the R3 ids, and the header nav has a link to each of the six non-hero sections.
Verdict: PASS
Evidence: section ids in document order: `["hero","about","services","process","team","testimonials","contact"]`. Header nav hrefs: `["#about","#services","#process","#team","#testimonials","#contact"]`.

## AC4: `lang="th"`, one `h1`, and the first Tab press focuses a skip link whose target is the main content.
Verdict: PASS
Evidence: `lang: th`, `h1 count: 1`. First Tab: `{tag:"A", cls:"skip-link", href:"#main", text:"ข้ามไปยังเนื้อหาหลัก", visible:[8,8,182,46]}`. Pressing Enter: `{hash:"#main", active:"MAIN#main"}` (`<main id="main" tabindex="-1">`). Same on 404.html (`404 first tab: skip-link #main`).

## AC5: Each fact from the Company facts list is present verbatim in the page text; the page contains no phone number or email address other than the facts; the footer has the fictional-company notice.
Verdict: PASS
Evidence: 36 fact strings checked (name in both forms and the combined form, tagline, 2016, the full About sentence, each service name and description, the four process steps, each team name and role, each quote and its source, address, phone, email, hours) against `document.body.textContent`: `facts missing (textContent): []`. Emails in source: `["hello@doiphraohill.example"]`; phone-like strings in text: `["053 000 4567"]`; tel hrefs: `tel:0530004567` (same number). Footer: "ดอยพร้าวฮิลล์ โรสเตอร์ส เป็นบริษัทสมมติ เว็บไซต์นี้จัดทำขึ้นเพื่อการสาธิตเท่านั้น ข้อมูลทั้งหมดไม่ใช่ข้อมูลจริง".
Note: the combined name "ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)" is in the text (footer, title, og:title, JSON-LD), but in the footer the English part is `display:block`, so the rendered `innerText` breaks it over two lines. The requirements are also ambiguous about services: the fact list writes "name: description". The page shows the name (h3) and description (p) separately, each verbatim, never joined with the colon. I counted that as verbatim.

## AC6: `scrollWidth` does not exceed the viewport width at 360, 768 and 1280 px.
Verdict: PASS
Evidence: `documentElement.scrollWidth` equals the viewport width for both pages in both themes at 320, 360, 375, 768, 1024, 1280 and 1440 (for example `index.html 360 light: {sw:360, cw:360}`, `768: {sw:768}`, `1280: {sw:1280}`). A separate text-extent scan found no text node closer than 12 px to either viewport edge at any of these widths. The only internal overflow is the decorative topo SVG inside `.hero { overflow:hidden }`.

## AC7: At 375 px the menu button starts with `aria-expanded="false"`, `aria-controls` names the nav element, a click and an Enter press each toggle it, and Escape closes it with focus returning to the button. At 1280 px the nav links are visible and the button is not.
Verdict: PASS
Evidence (375 px): initial `{expanded:"false", controls:"site-nav", controlsTag:"NAV", navVisible:false}`. Click -> `expanded:"true", navVisible:true`; second click -> `false`. Enter -> `true`; Enter -> `false`; Space -> `true`. With focus moved into the menu (`<a href="#services">`), Escape -> `{expanded:"false", navVisible:false, active:"menu-toggle"}`. At 767 px the button shows (`display:flex`) and the links are hidden. At 768 and 1280 px: `btnDisplay:"none"`, all six links visible in the viewport. Clicking a menu link also closes the menu.

## AC8: axe-core 4.10 reports zero violations on `index.html` in light and dark color schemes.
Verdict: PASS
Evidence: `axe.version 4.10.2`. `violations: []` for index.html light and dark at 375 and 1280 px. Also zero with the mobile menu open and with all three form errors shown, in both themes, and zero on 404.html. axe left `color-contrast` as "incomplete" on nodes over gradients or pseudo-element backgrounds (hero text, the lot tag, the cups, the desktop nav). I computed those pairs by hand, all at or above 4.5:1: tag muted on kraft 5.25 (light) and 5.54 (dark); hero muted on mist 6.07 and 7.7; cherry h1 accent on mist 5.55 and 6.51; primary button text 6.4 and 7.57; step numbers 5.08 and 6.13; cup initials 6.64 or more.

## AC9: The R10 metadata is present, the description length is 50 to 160 characters, and the JSON-LD values equal the facts.
Verdict: PASS
Evidence: title `ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters) | กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ`. The meta description is 110 characters. `og:title`, `og:description` and `og:type`=`website` are present. JSON-LD: `@type:"Organization"`, `name:"ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)"`, `telephone:"053 000 4567"`, `email:"hello@doiphraohill.example"`, `address:"99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190"`. All equal the facts. The address is a plain string, not a PostalAddress, which is valid schema.org.

## AC10: An empty submit shows a Thai error for each of the three fields with `aria-invalid="true"` and `aria-describedby` pointing at the message, and the page does not navigate. A valid submit navigates to a `mailto:hello@doiphraohill.example` URL whose subject decodes to `ติดต่อจากเว็บไซต์` and whose body contains the typed message.
Verdict: PASS
Evidence: empty submit gives name `aria-invalid="true"` with describedby `name-error` "กรุณากรอกชื่อของคุณหรือชื่อร้าน"; email with `email-error` "กรุณากรอกอีเมล"; message with `message-error` "กรุณากรอกข้อความที่ต้องการส่งถึงเรา". Each message is visible and sits in the same `.field` as its input. URL unchanged, `framenavigated` count 0, focus on `#name`. Valid submit: a navigation request to `mailto:hello@doiphraohill.example?subject=...&body=...` decodes to `subject: "ติดต่อจากเว็บไซต์"` and `body: "อยากสั่งกาแฟ 5 กิโล & ทดสอบ?=#\n\nชื่อ: คุณสมชาย\nอีเมลติดต่อกลับ: somchai@example.com"`. The `& ? = #` characters in the message survive encoding.

## AC11: There are no `<img>` elements and no image files, and each team member's initials are shown.
Verdict: PASS
Evidence: `img count: 0` on both pages; no image files. Initials shown: "ปว | ปาริชาติ วงศ์คำ", "ธส | ธนกร แสนดี", "มจ | มยุรี ใจงาม", "สท | สมเกียรติ ทองมา". All icons are inline SVG. The favicon is an inline data: SVG, not a file.

## AC12: With reduced motion emulated, no element has a non-zero transition or animation duration.
Verdict: PASS
Evidence: computed style scan of every element plus its ::before and ::after under `reducedMotion:'reduce'`: index.html `{bad:[], count:342, anims:0, scrollBehavior:"auto"}`, 404.html `{bad:[], anims:0}`; with the menu open `anims: 0`. Control run with no preference: `anims count 2` (ridge draw, topo rise), so the reduced-motion override is doing the work.

## AC13: Every executable `<script>` (anything except JSON-LD data blocks) has `defer` or `type="module"`.
Verdict: PASS
Evidence: index.html has two scripts: `application/ld+json` (data) and `src:"main.js", defer:true`. 404.html has no scripts.

## AC14: `404.html` has `lang="th"`, uses `styles.css`, and links to `index.html`.
Verdict: PASS
Evidence: `{lang:"th", css:["styles.css"], indexLinks:["ดอยพร้าวฮิลล์ โรสเตอร์ส ...(brand)", "กลับสู่หน้าแรก"], h1:1}`. The text is entirely Thai apart from the brand's English name. It uses the same header, topo, ridge and footer as the main page.

## Advisory

### AC15 [judgment]: At 375 and 1280 px the page looks finished and intentional.
Verdict: PASS (advisory)
Rationale: both widths look like a finished site. Nothing overlaps or clips. Thai line breaking is tidy because `.kw` nowrap phrases prevent the usual bad splits (for example ทุก|ล็อต). Line-height is 1.6 to 1.75. The hierarchy is clear: an 800-weight h1 against a 500-weight cherry second line, h2 sizes from 30 to 46 px, small muted kickers. The worst issue is at 1280: the contact column has a dead gap of about 150 px between the lead and the contact list, because the list is pinned to the bottom to line up with the form. The gap grows when the form shows errors.

### AC16 [judgment]: A visitor would remember the site.
Verdict: PASS (advisory)
Rationale: this does not read as a template. Several elements are specific to a hill roaster:
- A topographic contour map behind the hero.
- A kraft lot tag on a string that carries 2016, 120 shops, 48 hours and the phone number, set in monospace like a stamped label.
- A ridge-line skyline closing the hero, and a dark footer ridge.
- The process drawn as an actual roast curve: the turning-point dip, then a rise, with the four steps placed on it.
- Team initials served in espresso cups seen from above.
- A coffee-cherry dot before every kicker, and a perforated order-slip edge on the form.

The palette comes from the subject: mist green, cherry red, kraft, forest, roast brown. The section layouts all differ: split hero with tag, statement plus ledger, sticky heading plus menu-board rows, chart band, cup grid, asymmetric 7/5 quotes with a large lead quote, and info/form split. The weakest parts are the team row, which is sparse and small at desktop, and the reuse of the same hairline-ruled list idiom in about, services and contact.

### AC17 [judgment]: The details feel crafted in both themes.
Verdict: PASS (advisory), with dark-theme nits
Rationale: there is a single `--s-1..--s-9` spacing scale (4 to 96 px), used for nearly all padding and gaps. Hover states are consistent: cherry underline grow on nav links, darker cherry on buttons, an arrow nudge, a cherry border on the ghost button. Focus rings are 2 px cherry, recoloured to gold on the forest and roast bands and to dark ink on the kraft tag. The dark theme is designed rather than inverted: deep forest and roast surfaces, the tag keeps its kraft colour, and the cups keep porcelain and coffee. Several details are lost or slightly off, though (see nits 3 to 7 below).

### Nits (all seen in screenshots; none counted as failures)
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

## Other observations
- I also tested the must-haves with inputs of my own, and all held. R6 holds at 320, 375, 1024 and 1440 too. R7: Space toggles the menu, clicking a menu link closes it, and at 767 px the button shows. R9: axe is clean on 404.html, with the menu open, and with errors shown. R11: invalid emails `abc@` and `a b@c.d` and whitespace-only name and message each get the right Thai error; special characters survive mailto encoding; errors clear after a valid submit. R5: no invented claims; extra copy such as "สำหรับร้านกาแฟและออฟฟิศ" comes from the Goal. R15: the 404 page shares the header, topo, ridge and footer.
- No console errors or page errors on load.
- `reqs.md` sits at the project root next to the site. It is not a runtime file, but it will deploy with the site if the folder is uploaded as is.
