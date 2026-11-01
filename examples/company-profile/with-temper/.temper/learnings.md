# Learnings

บทเรียนที่ใช้ได้กับงานอื่นใน project นี้ ใส่ run id ที่สอนบทเรียนนั้นไว้ด้วย

## 2026-11-01

- Thai line breaking: Chromium's dictionary splits some loanwords and compounds in the wrong place (ทุกล็อต, บาริสต้า, ลาเต้อาร์ต, บรรจุภัณฑ์). Keep such short phrases together with an inline `white-space: nowrap` span, never `display: inline-block`, which strands whole fragments on their own lines in narrow columns. (run 001, v1 to v2)
- Check the layout at 1024 px as well as 375 px and 1280 px: multi-column cards are at their narrowest there, and that is where the v1 wrapping problems showed. (run 001)
