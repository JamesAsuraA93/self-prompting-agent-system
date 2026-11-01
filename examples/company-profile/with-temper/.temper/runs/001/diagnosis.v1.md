# Diagnosis v1

Hard criteria: 14 of 14 passed. Advisory AC15 failed.
Decision from the script: pass_with_advisory. Continuing to v2 because the user's standing instruction is to be picky about UI and fix anything that looks off.

## AC15: execution slip
Evidence: judge.v1.md, AC15. At 1280 px Thai text in the four-column cards breaks badly: "ตรวจคุณภาพทุ / กล็อต" in process step 3, "คอร์สลาเต้ / อาร์ต" leaving a one-word line in the barista card, and "เครื่อง / ชง" leaving a one-syllable line in the machine care card. The same cards run to three lines at 1024 px.
Cause: the executor wrapped Thai phrases in `.nb` spans with `display:inline-block` to stop mid-word breaks at 375 px. Inline-block fragments cannot wrap, so in narrow columns the browser pushes whole fragments onto their own lines and splits the remaining text wherever it can.
The prompt asked the executor to look at 375 px and 1280 px, and it did, but it did not check the 1024 px to 1280 px range where the cards are narrowest, and it judged its own fix at 375 px only.
Change in v2: state that the site exists and passes every hard criterion, name the three broken breaks and their cause, ask for natural Thai line breaking at every width from 360 px to 1440 px without changing the text, and add 1024 px and 1440 px to the visual check.
