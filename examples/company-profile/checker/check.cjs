// ตรวจเว็บ company profile ตาม AC1 - AC14 ของ reqs.md แล้วพิมพ์ผลเป็น JSON
// ใช้: node check.cjs <site-dir> [screenshot-dir]
const fs = require("fs");
const path = require("path");
const http = require("http");
const { chromium } = require("playwright");

const SITE = path.resolve(process.argv[2]);
const SHOTS = process.argv[3] ? path.resolve(process.argv[3]) : null;
const AXE = require.resolve("axe-core/axe.min.js", { paths: [__dirname] });

const FACTS = [
  "ดอยพร้าวฮิลล์ โรสเตอร์ส", "Doi Phrao Hill Roasters", "กาแฟคั่วสดจากดอย ส่งตรงถึงร้านคุณ", "2016",
  "โรงคั่วกาแฟพิเศษในอำเภอพร้าว จังหวัดเชียงใหม่ รับซื้อเมล็ดตรงจากเกษตรกรบนดอย และส่งกาแฟคั่วสดให้ร้านกาแฟกว่า 120 ร้าน",
  "คั่วกาแฟสำหรับร้าน", "คั่วตามโปรไฟล์ที่ร้านเลือก ส่งทุกสัปดาห์",
  "กาแฟ Private Label", "กาแฟคั่วพร้อมบรรจุภัณฑ์ในแบรนด์ของคุณเอง",
  "อบรมบาริสต้า", "คอร์สพื้นฐานและคอร์สลาเต้อาร์ตสำหรับทีมหน้าร้าน",
  "ดูแลเครื่องชง", "ตรวจเช็คและปรับตั้งเครื่องชงถึงหน้าร้าน",
  "คัดเมล็ดจากเกษตรกร", "คั่วตามโปรไฟล์", "Cupping ตรวจคุณภาพทุกล็อต", "ส่งถึงร้านภายใน 48 ชั่วโมงหลังคั่ว",
  "ปาริชาติ วงศ์คำ", "ผู้ก่อตั้งและหัวหน้าโรงคั่ว", "ธนกร แสนดี", "Q Grader", "มยุรี ใจงาม", "หัวหน้าฝ่ายอบรม", "สมเกียรติ ทองมา", "ฝ่ายดูแลลูกค้า",
  "เมล็ดสดทุกล็อต ลูกค้าประจำสังเกตได้เลยว่ารสชาติคงที่ขึ้น", "ร้านบ้านไม้ คาเฟ่",
  "ทีมอบรมใจเย็นมาก บาริสต้าใหม่ของเราชงได้มาตรฐานภายในสองสัปดาห์", "ร้านลมหนาว",
  "สั่งวันจันทร์ ได้ของวันพุธ ไม่เคยพลาดสักครั้ง", "ออฟฟิศสวนสัก",
  "99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190", "053 000 4567", "hello@doiphraohill.example", "จันทร์ - เสาร์ 8:30 - 17:30",
];
const EMAIL = "hello@doiphraohill.example";
const SECTIONS = ["hero", "about", "services", "process", "team", "testimonials", "contact"];
const RUNTIME_EXT = /\.(html?|css|m?js|json|svg|png|jpe?g|gif|webp|avif|ico|woff2?|ttf|otf)$/i;
const IMAGE_EXT = /\.(svg|png|jpe?g|gif|webp|avif|ico)$/i;
const results = [];
const check = (text, passed, evidence) => results.push({ text, passed: Boolean(passed), evidence: String(evidence).slice(0, 400) });
const norm = (s) => s.replace(/\s+/g, " ").trim();

// 1. static server เล็ก ๆ สำหรับเสิร์ฟโฟลเดอร์
function serve(dir) {
  const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".mjs": "text/javascript", ".svg": "image/svg+xml" };
  const server = http.createServer((req, res) => {
    const rel = decodeURIComponent(new URL(req.url, "http://x").pathname);
    let file = path.join(dir, rel.endsWith("/") ? rel + "index.html" : rel);
    if (!file.startsWith(dir) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404, { "content-type": "text/html; charset=utf-8" });
      return res.end(fs.existsSync(path.join(dir, "404.html")) ? fs.readFileSync(path.join(dir, "404.html")) : "not found");
    }
    res.writeHead(200, { "content-type": types[path.extname(file)] || "application/octet-stream" });
    res.end(fs.readFileSync(file));
  });
  return new Promise((r) => server.listen(0, "127.0.0.1", () => r(server)));
}

function walk(dir, base = dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    if ([".temper", "node_modules", ".git"].includes(e.name)) return [];
    const p = path.join(dir, e.name);
    return e.isDirectory() ? walk(p, base) : [path.relative(base, p)];
  });
}

(async () => {
  // 2. AC1 ไฟล์และขนาด
  const required = ["index.html", "404.html", "styles.css", "main.js"];
  const files = fs.existsSync(SITE) ? walk(SITE) : [];
  const missing = required.filter((f) => !files.includes(f));
  const extra = files.filter((f) => RUNTIME_EXT.test(f) && !required.includes(f));
  const size = required.filter((f) => files.includes(f)).reduce((n, f) => n + fs.statSync(path.join(SITE, f)).size, 0);
  check("AC1: the four files exist at the root", missing.length === 0, `missing ${JSON.stringify(missing)}`);
  check("AC1: no other runtime files", extra.length === 0, `extra ${JSON.stringify(extra)}`);
  check("AC1: total size under 100 KB", size < 100 * 1024 && missing.length === 0, `${size} bytes`);
  if (missing.includes("index.html")) { console.log(JSON.stringify(results)); return; }

  const server = await serve(SITE);
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch();
  const external = [];
  const mailtos = [];
  const newPage = async (opts = {}) => {
    const ctx = await browser.newContext(opts);
    ctx.on("request", (r) => {
      const u = r.url();
      if (u.startsWith("mailto:")) mailtos.push(u);
      else if (/^https?:/.test(u) && !u.startsWith(origin)) external.push(u);
    });
    return ctx.newPage();
  };

  try {
    let page = await newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto(origin + "/index.html", { waitUntil: "networkidle" });

    // 3. AC3 sections และ nav
    const sec = await page.evaluate((ids) => {
      const els = ids.map((id) => document.getElementById(id));
      const missing = ids.filter((id, i) => !els[i]);
      const present = els.filter(Boolean);
      const ordered = present.every((el, i) => i === 0 || present[i - 1].compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING);
      const header = document.querySelector("header");
      const navMissing = ids.slice(1).filter((id) => !(header && header.querySelector(`a[href="#${id}"]`)));
      return { missing, ordered, navMissing };
    }, SECTIONS);
    check("AC3: seven sections exist with the R3 ids", sec.missing.length === 0, `missing ${JSON.stringify(sec.missing)}`);
    check("AC3: sections are in the R3 order", sec.ordered && sec.missing.length === 0, `ordered=${sec.ordered}`);
    check("AC3: header nav links to the six non-hero sections", sec.navMissing.length === 0, `missing links ${JSON.stringify(sec.navMissing)}`);

    // 4. AC4 lang, h1, skip link
    const basics = await page.evaluate(() => ({ lang: document.documentElement.lang, h1: document.querySelectorAll("h1").length }));
    check('AC4: <html lang="th">', basics.lang === "th", `lang=${basics.lang}`);
    check("AC4: exactly one h1", basics.h1 === 1, `h1 count ${basics.h1}`);
    await page.keyboard.press("Tab");
    const skip = await page.evaluate(() => {
      const a = document.activeElement;
      if (!a || a.tagName !== "A") return { ok: false, why: `focused ${a && a.tagName}` };
      const href = a.getAttribute("href") || "";
      const target = href.startsWith("#") ? document.getElementById(href.slice(1)) : null;
      const isMain = target && (target.tagName === "MAIN" || target.getAttribute("role") === "main" || target.closest("main") || target.querySelector("main"));
      return { ok: Boolean(isMain), why: `href=${href} target=${target && target.tagName}` };
    });
    check("AC4: first Tab focuses a skip link to the main content", skip.ok, skip.why);

    // 5. AC5 facts, เบอร์และอีเมลอื่น, footer notice
    const text = norm(await page.evaluate(() => document.body.innerText));
    const html = await page.content();
    const missingFacts = FACTS.filter((f) => !text.includes(norm(f)));
    check("AC5: every company fact appears verbatim", missingFacts.length === 0, `missing ${JSON.stringify(missingFacts)}`);
    const emails = [...new Set((html.match(/[\w.+-]+@[\w-]+(\.[\w-]+)+/g) || []).map((e) => e.toLowerCase()))].filter((e) => !/\.(png|svg|css|js)$/.test(e));
    const phones = [...new Set([...text.matchAll(/(?:\+66|0)\d{1,2}[\s-]?\d{3}[\s-]?\d{3,4}/g)].map((m) => m[0].replace(/\D/g, "").replace(/^66/, "0")))];
    const telLinks = await page.evaluate(() => [...document.querySelectorAll('a[href^="tel:"]')].map((a) => a.getAttribute("href")));
    const telDigits = telLinks.map((t) => t.replace(/\D/g, "").replace(/^66/, "0"));
    check("AC5: no email address other than the facts", emails.every((e) => e === EMAIL), `emails ${JSON.stringify(emails)}`);
    check("AC5: no phone number other than the facts", [...phones, ...telDigits].every((p) => p === "0530004567"), `phones ${JSON.stringify(phones)} tel ${JSON.stringify(telLinks)}`);
    const footer = norm(await page.evaluate(() => (document.querySelector("footer") || {}).innerText || ""));
    check("AC5: footer has a Thai fictional-company notice", /สมมติ|สมมุติ/.test(footer) && /ตัวอย่าง|สาธิต|เดโม|demo/i.test(footer), footer.slice(0, 200));

    // 6. AC9 metadata
    const meta = await page.evaluate(() => {
      const m = (sel) => (document.querySelector(sel) || {}).content || "";
      const lds = [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => { try { return JSON.parse(s.textContent); } catch { return null; } });
      return { title: document.title, desc: m('meta[name="description"]'), ogt: m('meta[property="og:title"]'), ogd: m('meta[property="og:description"]'), ogtype: m('meta[property="og:type"]'), lds };
    });
    check("AC9: title contains the company name", /ดอยพร้าวฮิลล์|Doi Phrao Hill/.test(meta.title), meta.title);
    check("AC9: meta description is 50 to 160 characters", meta.desc.length >= 50 && meta.desc.length <= 160, `${meta.desc.length} chars`);
    check("AC9: og:title, og:description and og:type are set", meta.ogt && meta.ogd && meta.ogtype, JSON.stringify([meta.ogt, meta.ogd, meta.ogtype]));
    const flat = (x) => (Array.isArray(x) ? x.flatMap(flat) : x && x["@graph"] ? flat(x["@graph"]) : x ? [x] : []);
    const org = meta.lds.flatMap(flat).find((o) => o && [].concat(o["@type"]).some((t) => /Organization|LocalBusiness|Store|CafeOrCoffeeShop/.test(t)));
    const names = ["ดอยพร้าวฮิลล์ โรสเตอร์ส", "Doi Phrao Hill Roasters", "ดอยพร้าวฮิลล์ โรสเตอร์ส (Doi Phrao Hill Roasters)"];
    const addrText = org ? norm(typeof org.address === "string" ? org.address : Object.entries(org.address || {}).filter(([k]) => !k.startsWith("@")).map(([, v]) => v).join(" ")) : "";
    const addrOk = "99/9 หมู่ 5 ตำบลสมมติ อำเภอพร้าว จังหวัดเชียงใหม่ 50190".split(" ").every((tok) => addrText.includes(tok));
    const ldOk = org && names.includes(norm(org.name || "")) && String(org.telephone || "").replace(/\D/g, "").replace(/^66/, "0") === "0530004567" && org.email === EMAIL && addrOk;
    check("AC9: JSON-LD Organization name, telephone, email and address match the facts", ldOk, org ? JSON.stringify({ name: org.name, telephone: org.telephone, email: org.email, address: addrText }) : "no Organization JSON-LD");

    // 7. AC11 รูปภาพและ initials
    const imgs = await page.evaluate(() => document.querySelectorAll("img").length);
    const imageFiles = files.filter((f) => IMAGE_EXT.test(f));
    check("AC11: no <img> elements and no image files", imgs === 0 && imageFiles.length === 0, `img=${imgs} files=${JSON.stringify(imageFiles)}`);
    const initials = await page.evaluate(() => {
      const team = document.getElementById("team");
      if (!team) return [];
      return [...team.querySelectorAll("*")].map((el) => (el.children.length === 0 ? el.textContent.replace(/\s/g, "") : "")).filter((t) => t.length >= 1 && t.length <= 3);
    });
    const firsts = ["ป", "ธ", "ม", "ส"];
    check("AC11: each team member's initials are shown", firsts.every((c) => initials.some((t) => t.startsWith(c))), `short texts in #team ${JSON.stringify(initials.slice(0, 12))}`);

    // 8. AC13 scripts
    const scripts = await page.evaluate(() => [...document.querySelectorAll("script")].filter((s) => s.type !== "application/ld+json").map((s) => ({ src: s.getAttribute("src"), defer: s.defer, module: s.type === "module" })));
    check("AC13: every script uses defer or type=module", scripts.every((s) => s.defer || s.module), JSON.stringify(scripts));

    // 9. AC7 desktop nav
    const desk = await page.evaluate(() => {
      const header = document.querySelector("header");
      const btn = header && header.querySelector("button[aria-controls]");
      const vis = (el) => el && el.getClientRects().length > 0 && getComputedStyle(el).visibility !== "hidden";
      const links = header ? [...header.querySelectorAll('a[href^="#"]')].filter((a) => a.getAttribute("href") !== "#main" && a.getAttribute("href").length > 1) : [];
      return { btnVisible: vis(btn), linksVisible: links.filter(vis).length };
    });
    check("AC7: at 1280 px the nav links are visible and the menu button is not", !desk.btnVisible && desk.linksVisible >= 6, JSON.stringify(desk));

    // 10. AC6 horizontal scroll
    const overflow = [];
    for (const w of [360, 768, 1280]) {
      await page.setViewportSize({ width: w, height: 800 });
      await page.waitForTimeout(150);
      const sw = await page.evaluate(() => document.documentElement.scrollWidth);
      if (sw > w) overflow.push(`${w}: scrollWidth ${sw}`);
    }
    check("AC6: no horizontal scroll at 360, 768 and 1280 px", overflow.length === 0, overflow.join("; ") || "ok");

    // 11. AC8 axe ทั้งสอง theme
    // โหลดหน้าใหม่ใน scheme นั้นตั้งแต่ต้น ไม่สลับกลางทาง เพราะ CSS transition ของสีทำให้ axe วัด contrast ระหว่างเปลี่ยนสีแล้วผลไม่นิ่ง
    for (const scheme of ["light", "dark"]) {
      const ap = await newPage({ viewport: { width: 1280, height: 900 }, colorScheme: scheme });
      await ap.goto(origin + "/index.html", { waitUntil: "networkidle" });
      await ap.waitForTimeout(1000);
      await ap.addScriptTag({ path: AXE });
      const v = await ap.evaluate(async () => (await axe.run(document)).violations.map((x) => `${x.id}(${x.nodes.length}): ${x.nodes.slice(0, 2).map((n) => n.target.join(" ")).join(" | ")}`));
      check(`AC8: axe-core reports zero violations in ${scheme} mode`, v.length === 0, v.join("; ") || "none");
    }

    // 12. AC12 reduced motion
    await page.emulateMedia({ reducedMotion: "reduce", colorScheme: "light" });
    const moving = await page.evaluate(() => {
      const nonzero = (v) => v.split(",").some((d) => parseFloat(d) > 0);
      const out = [];
      for (const el of document.querySelectorAll("*")) {
        for (const pseudo of [null, "::before", "::after"]) {
          const cs = getComputedStyle(el, pseudo);
          if (nonzero(cs.transitionDuration) || (cs.animationName !== "none" && nonzero(cs.animationDuration))) out.push(`${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""}${el.className && typeof el.className === "string" ? "." + el.className.split(" ")[0] : ""}${pseudo || ""}`);
        }
      }
      return out;
    });
    check("AC12: nothing transitions or animates with reduced motion", moving.length === 0, moving.slice(0, 8).join(", ") || "none");

    // 13. AC7 mobile nav
    page = await newPage({ viewport: { width: 375, height: 800 } });
    await page.goto(origin + "/index.html", { waitUntil: "networkidle" });
    const btnSel = "header button[aria-controls]";
    const hasBtn = await page.$(btnSel);
    if (!hasBtn) {
      check("AC7: mobile menu button with aria-expanded and aria-controls", false, "no header button[aria-controls]");
    } else {
      const state = () => page.$eval(btnSel, (b) => {
        const t = document.getElementById(b.getAttribute("aria-controls"));
        return { exp: b.getAttribute("aria-expanded"), target: t ? t.tagName : null, targetVisible: Boolean(t && t.getClientRects().length && getComputedStyle(t).visibility !== "hidden"), focused: document.activeElement === b };
      });
      const s0 = await state();
      check("AC7: menu button starts collapsed and controls the nav", s0.exp === "false" && s0.target && !s0.targetVisible, JSON.stringify(s0));
      await page.click(btnSel); const s1 = await state();
      await page.click(btnSel); const s2 = await state();
      check("AC7: click toggles the menu open and closed", s1.exp === "true" && s1.targetVisible && s2.exp === "false" && !s2.targetVisible, JSON.stringify([s1, s2]));
      await page.focus(btnSel); await page.keyboard.press("Enter"); const s3 = await state();
      await page.keyboard.press("Escape"); const s4 = await state();
      check("AC7: Enter opens, Escape closes and focus returns to the button", s3.exp === "true" && s3.targetVisible && s4.exp === "false" && !s4.targetVisible && s4.focused, JSON.stringify([s3, s4]));
      await page.focus(btnSel); await page.keyboard.press("Space"); const s5 = await state();
      await page.keyboard.press("Escape");
      check("AC7: Space opens the menu", s5.exp === "true" && s5.targetVisible, JSON.stringify(s5));
    }

    // 14. AC10 form
    page = await newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto(origin + "/index.html", { waitUntil: "networkidle" });
    const form = await page.$("#contact form");
    if (!form) {
      check("AC10: contact form exists in #contact", false, "no form");
    } else {
      const fieldSel = {
        name: '#contact form input:not([type="email"]):not([type="hidden"]):not([type="submit"]):not([type="checkbox"])',
        email: '#contact form input[type="email"], #contact form input[name*="mail" i]',
        message: "#contact form textarea",
      };
      let navigations = 0;
      page.on("framenavigated", (f) => { if (f === page.mainFrame()) navigations++; });
      const submit = '#contact form [type="submit"], #contact form button:not([type="button"])';
      await page.click(submit);
      await page.waitForTimeout(300);
      const errs = {};
      for (const [k, sel] of Object.entries(fieldSel)) {
        errs[k] = await page.evaluate((sel) => {
          const el = document.querySelector(sel);
          if (!el) return { ok: false, why: "field not found" };
          const ids = (el.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean);
          const msgs = ids.map((id) => document.getElementById(id)).filter((m) => m && m.getClientRects().length && /[฀-๿]/.test(m.textContent));
          return { ok: el.getAttribute("aria-invalid") === "true" && msgs.length > 0, why: `aria-invalid=${el.getAttribute("aria-invalid")} describedby=${ids.join(",")} msg=${msgs.map((m) => m.textContent.trim()).join("|")}` };
        }, sel);
      }
      check("AC10: empty submit shows Thai errors with aria-invalid and aria-describedby on all three fields", Object.values(errs).every((e) => e.ok), JSON.stringify(errs));
      check("AC10: empty submit does not navigate or open mail", navigations === 0 && mailtos.length === 0, `navigations=${navigations} mailtos=${mailtos.length}`);
      await page.fill(fieldSel.name, "ทดสอบ ระบบ");
      await page.fill(fieldSel.email, "abc");
      await page.fill(fieldSel.message, "ขอใบเสนอราคากาแฟ 5 กิโล");
      await page.click(submit); await page.waitForTimeout(300);
      const badEmail = await page.$eval(fieldSel.email, (el) => el.getAttribute("aria-invalid"));
      check("AC10: an invalid email is flagged", badEmail === "true" && mailtos.length === 0, `aria-invalid=${badEmail} mailtos=${mailtos.length}`);
      await page.fill(fieldSel.email, "owner@cafe.example");
      await page.click(submit); await page.waitForTimeout(500);
      const m = mailtos[0];
      let ok = false, why = "no mailto navigation";
      if (m) {
        const u = new URL(m);
        const subject = u.searchParams.get("subject");
        const body = u.searchParams.get("body") || "";
        ok = decodeURIComponent(u.pathname).toLowerCase() === EMAIL && subject === "ติดต่อจากเว็บไซต์" && body.includes("ขอใบเสนอราคากาแฟ 5 กิโล");
        why = `to=${decodeURIComponent(u.pathname)} subject=${subject} body=${body.slice(0, 80)}`;
      }
      check("AC10: a valid submit opens the right mailto with subject and message", ok, why);
    }

    // 15. AC14 404
    page = await newPage({ viewport: { width: 1280, height: 900 } });
    if (files.includes("404.html")) {
      await page.goto(origin + "/404.html", { waitUntil: "networkidle" });
      const p404 = await page.evaluate(() => ({
        lang: document.documentElement.lang,
        css: [...document.querySelectorAll('link[rel="stylesheet"]')].some((l) => /styles\.css$/.test(l.getAttribute("href"))),
        home: [...document.querySelectorAll("a[href]")].some((a) => ["index.html", "./index.html", "/index.html", "./", "/"].includes(a.getAttribute("href"))),
        thai: /[฀-๿]/.test(document.body.innerText),
      }));
      check("AC14: 404.html is Thai, uses styles.css and links to index.html", p404.lang === "th" && p404.css && p404.home && p404.thai, JSON.stringify(p404));
    } else {
      check("AC14: 404.html is Thai, uses styles.css and links to index.html", false, "404.html missing");
    }

    // 16. AC2 external requests (เก็บมาตลอดทุกหน้า)
    check("AC2: no request leaves the local server", external.length === 0, JSON.stringify([...new Set(external)].slice(0, 5)));

    // 17. screenshots สำหรับดูด้วยตา
    if (SHOTS) {
      fs.mkdirSync(SHOTS, { recursive: true });
      for (const [w, scheme] of [[375, "light"], [375, "dark"], [1280, "light"], [1280, "dark"]]) {
        const p = await newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
        await p.goto(origin + "/index.html", { waitUntil: "networkidle" });
        await p.screenshot({ path: path.join(SHOTS, `index-${w}-${scheme}.png`), fullPage: true });
      }
      const p = await newPage({ viewport: { width: 375, height: 800 } });
      await p.goto(origin + "/index.html", { waitUntil: "networkidle" });
      if (await p.$(btnSel)) { await p.click(btnSel); await p.screenshot({ path: path.join(SHOTS, "menu-open-375.png") }); }
      await p.goto(origin + "/404.html", { waitUntil: "networkidle" });
      await p.screenshot({ path: path.join(SHOTS, "404-375.png"), fullPage: true });
    }
  } catch (e) {
    check("checker ran to completion", false, e.stack || e.message);
  } finally {
    await browser.close();
    server.close();
  }
  console.log(JSON.stringify(results, null, 1));
})();
