# Learnings

บทเรียนที่ใช้ได้กับงานอื่นใน project นี้ ใส่ run id ที่สอนบทเรียนนั้นไว้ด้วย

## 2026-11-01

- Thai line breaking: Chromium's dictionary splits some loanwords and compounds in the wrong place (ทุกล็อต, บาริสต้า, ลาเต้อาร์ต, บรรจุภัณฑ์). Keep such short phrases together with an inline `white-space: nowrap` span, never `display: inline-block`, which strands whole fragments on their own lines in narrow columns. (run 001, v1 to v2)
- Check the layout at 1024 px as well as 375 px and 1280 px: multi-column cards are at their narrowest there, and that is where the v1 wrapping problems showed. (run 001)

## 2026-11-01 (run 003-design)

- Taste only shows up when reqs.md asks for it. The first two runs passed "looks finished" with a forgettable template; stating a design identity as `[judgment]` criteria (R16, AC16, AC17) is what moved it. (run 003-design)
- In dark mode, check decorative outlines and card edges against their own background, not only text contrast: the judge measured the footer hill outline and the form card edge at 1.02:1 and 1.03:1, which axe does not flag. (run 003-design)
- After a failed form submit, give fields a `scroll-margin-top` equal to the sticky header height, or the focused field's label lands under the header. (run 003-design)
