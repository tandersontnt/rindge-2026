# Rindge Town Guide v9: Town reports page (Oct 11, 2026)

- **New chapter.** "Town reports" (`#reports`, section `#townreports`) sits after Documents. `src/reports.py` builds it from `docs/MANIFEST.json`.
- **2011 to 2025, complete.** There is one tile per year, newest first, for 15 reports, all from the town's Town Reports folder (checked Oct 9, 2026).
  - 12 reports open in the site's viewer from local copies.
  - 2012, 2014 and 2017 are over 25 MB and open on rindgenh.org.
  - The build fails if a year is duplicated, and the page lists any missing year automatically.
- **1849 to 2010.** Older reports are linked as collections, not year by year: UNH Scholars' Repository (`scholars.unh.edu/rindge_nh_reports/`, about 187 scans from 1849 to 2024), HathiTrust and the Internet Archive.
  - These sites were confirmed by web search. This cloud environment's network policy blocks scholars.unh.edu and rindgenh.org, so each year's item could not be opened and verified.
  - No per-year URL was guessed. With those hosts allowed, the UNH items can be listed by year.
- **Links into the chapter:** a Home "More questions" link, the menu and footer (automatic), and a search "Top hit" for "town report" and "annual report".
- **Design test:** covers the new chapter and adds a "Where are the annual town reports?" findability task. It passes with 0 failures and 0 warnings.

# Rindge Town Guide v8: structured data (Oct 11, 2026)

**Machine-readable layer.** `src/structured.py` runs at the end of `build.py`.

- **Office hours.** The posted hours of 10 offices are re-typed as rules, one to one with the text in `r3data.DEPTS`. Days the town does not post stay "not posted" and are never guessed: the Town Clerk's Friday, and Public Works on Fridays May–Oct. Planning's Thursday is by appointment.
- **schema.org JSON-LD** in the page head:
  - `WebSite`, with a `SearchAction` (`?q=`) and an unofficial-status disclaimer;
  - 16 `GovernmentOffice` / `Library` entries with phone, address, town page and non-seasonal opening hours, each with `parentOrganization` Town of Rindge;
  - a `FAQPage` of the 15 how-to guides, with answers taken from each guide's own summary;
  - a `Dataset` for `meetings.json`. No license is declared; that is the owner's decision.
- **No `Event` markup.** Most upcoming dates are inferred or derived, not posted by the town, and publishing them as events would present them as fact.

**On the page.** All of these are built in `app.js` from data already in the page:

- **Right now in Rindge** (Home): open/closed status for five places, computed in America/New_York time from the posted hours. A note says holidays are not included. Next to it, the next three dates from the calendar, with countdowns and their source labels.
- **Directory:** an open/closed status on each office with posted hours. It refreshes every minute.
- **Timeline:** a "2026 at a glance" grid of boards by months. Each cell filters the timeline to that board and jumps to that month.
- **Tables:** every data table has sortable columns (`aria-sort`; Total rows stay at the bottom) and a "Download CSV" button.
- **Search links:** `?q=word` opens search with that word.

**Design test:** a new `data` check validates the JSON-LD. It runs the open/closed logic at six fixed moments (weekday, a Friday with unposted hours, Sunday, a by-appointment day, winter and summer hours) and checks the countdown, the grid totals against the filter counts, numeric sorting and `?q=`. The full suite has 0 failures and 0 warnings.

# Rindge Town Guide v7: design test and deep polish (Oct 11, 2026)

**Design test.** `test/design_test.mjs` runs headless Chromium with axe-core across every chapter. It covers phone and desktop, light and dark: 40 views, plus reflow and search runs.

To run it: `PLAYWRIGHT=<path to playwright> AXE=<path to axe-core/axe.min.js> node test/design_test.mjs index.html`. Results are written to `test/design_results.json`.

| Check | What passes |
|---|---|
| axe | WCAG 2.0, 2.1 and 2.2 A/AA rules, with expanded cards included |
| structure | exactly one h1 per view and no skipped heading levels |
| focus | a visible focus ring on every tab stop |
| readability | no text under 12px; warnings for text under 14px and lines over 95 characters |
| targets | controls at least 24px (fail) and 44px (goal) |
| reflow | 320px wide, 200% text, and WCAG text-spacing override |
| charts | every bar with a value draws |
| findability | 16 common resident questions: a one-tap link from Home, and the first search result lands on the answer |

**Baseline v6:** 50 failures and 81 warnings.

**Final:** 0 failures and 0 warnings.

**Fixes:**
- **Chapter titles** are the page h1.
- **Text size:** there is a 14px floor for all text, including source labels.
- **Touch targets:** link lists, phone numbers and section tabs are 44px.
- **Line length:** notes are capped at 72 characters per line.
- **Search** matches whole words only ("rate" no longer matches "separate"). It ranks by relevance, and a "Top hit" row covers the most common resident questions.
- **Election result bars** were invisible because chart rows reused the top bar's `.bar` class. This was a bug that predates this work.
- **Chart colors** use a categorical palette that passes the colorblind and contrast checks in light and dark mode:
  - Town / local school / state education / county: `#2a78d6`, `#eb6834`, `#1baf7a`, `#eda100`.
  - Boards use the same order, with violet unused.
  - Text never uses a series color; a dot carries the color instead.
- **Calendar days** use a tinted cell with an ink number. Before, white text sat on the board color.
- **Home:** the facts line is plain text, and the label key is a clean two-column list.
- **Phone header:** the subtitle wraps instead of being cut off.

**No content changes.** No facts, labels or links were added or removed.

# Rindge Town Guide v6: design pass (Oct 11, 2026)

- **Chapter header.** Each chapter opens with a large title, a "‹ Home" back link and a one-line description, instead of a boxed card plus a breadcrumb. With JavaScript off, breadcrumbs still show.
- **Sticky section tabs.** Chapters with more than one section get a segmented control for their sections. It stays under the top bar and highlights the section in view. On phones it becomes a solid band under the top bar.
- **Quieter content chrome.**
  - The "In plain language" note is now text with an accent rule instead of a separate box.
  - Source labels are a coloured dot plus text, with no pill or outline.
  - The Share button is icon-only.
  - Shadows are lighter.
- **One accent colour.** Topic and how-to icons use the accent colour. Board colours appear only as dots in the timeline and its filter chips.
- **Inset grouped lists.** Topics and how-to guides each read as one rounded list with hairline dividers.
- **Fixes:** stat numbers no longer wrap ($19,904,756), and the cut-off "Source and …" text is gone from stat tiles.
- **No content changes.** No facts, labels or links were added or removed.

# Rindge Town Guide v5: navigation polish (Oct 11, 2026)

- **One chapter per screen (JavaScript only).** Home, or one group with its sections, is shown at a time, so links no longer scroll through the whole guide. Without JavaScript the full long page still works. Jumps between chapters are instant. Smooth scrolling is kept only for short moves within a chapter.
- **Back and Forward** restore your place on the chapter you came from (`history.scrollRestoration` is manual).
- **Previous and Next cards** appear at the end of every chapter.
- **Quick-call strip on Home:** 911, police non-emergency (603) 899-5009 and Town Offices (603) 899-5181, as tap-to-call links. The numbers are the same ones the guide already lists.
- **No focus ring on headings that navigation focuses.** Keyboard focus rings on controls are unchanged.
- **The "Top" button** goes to the top of the current chapter.
- **No repeated intros.** Each section's lead line gives the answer. The "In plain language" box now adds only details the lead line doesn't already state, and the grey note keeps only source and date details. No facts or source labels were removed.
- **The Document library is its own chapter** ("Documents" in the top bar and the menu). "Meetings and documents" became "Meetings and dates" (the timeline and the key dates).
- **Fix:** closing the document viewer now keeps the link that opened it on screen. Before, the browser's scroll restoration could move the page.

# Rindge Town Guide v3: audit (Oct 9, 2026, ET)

This section covers v3 and the round-3 content. The v2 and v1 audits follow below and still apply. To rebuild, run `python3 src/build.py`, which reads `data.py`, `v2data.py`, `lawdata.py`, `r3data.py`, `v2.py`, `v3.py` and `v3docs.py`. To add any newly cited town files to `docs/`, run `python3 src/fetch_docs.py` first. To run the tests, use `node --experimental-websocket test/cdp_test.mjs`, which writes `test/results_v3.json`.

## A. Documents inside the site
- **Framing test, done first.** rindgenh.org and rindgenh.gov send `X-Frame-Options: SAMEORIGIN` and CSP `frame-ancestors 'self'`, so their pages can't be framed from another site. Some other hosts refuse framing too:
  - SAMEORIGIN: gencourt (gc.nh.gov), townhallstreams, co.cheshire and census;
  - DENY: mytownview;
  - other blocks: citizenportal blocks framing, and nhdeeds shows a cookie wall.

  Headless Chrome did render three hosts in a frame: ledgertranscript.com, keenesentinel.com and nhmunicipal.org.
- **Copies.** 162 town files (156 PDFs and 6 Word files) are copied byte for byte into `docs/`. Together they are 181.6 MB in the manifest, or 175 MB on disk.
  - Every PDF was checked for the `%PDF` header.
  - `docs/MANIFEST.json` records each file's source URL, sha256, size, content type and retrieval date.
  - Each Word file also has a LibreOffice PDF rendering in `docs/converted/`, with its own sha256 and a note. The viewer shows the rendering, and Download gives the original Word file.
  - No document was altered.
  - Credit line: "Public record, copied from rindgenh.org on Oct 9, 2026; the original is authoritative."
- **Not copied (larger than 25 MB).** The 2012, 2014 and 2017 annual reports are listed in `not_copied` in the manifest. The viewer shows a card that opens them on rindgenh.org.
- **Missing at the source (404 on Oct 9).** The Select Board minutes of 3/25/2026 and rindgenh.gov `news_detail_T2_R16.php`. The viewer shows a "not available right now" card with the original link and the Town Offices phone number.
- **Viewer.** The viewer is full screen and shows:
  - the title, source URL, kind and "n of N";
  - Previous and Next;
  - "Open original on rindgenh.org", which names the actual host for other sources;
  - Download, for local copies only;
  - Close.

  It also handles keyboard and history:
  - Esc closes it, and focus returns to the link that opened it.
  - Focus is trapped inside it (26 Tab and Shift-Tab presses, 0 escapes).
  - The phone Back button closes it.

  If `navigator.pdfViewerEnabled` is false (for example on Android Chrome), the viewer shows a card with "Open the copy", "Open original" and "Download" instead of a blank frame.
- **Embeds.** Only the three tested hosts are framed, and they are sandboxed. Every other outside source gets an "Opens in a new tab" card, so no blank frames appear.
- **Without JavaScript.** Links in the timeline and elsewhere keep their original URLs. Library "View" links point to the local copy.
- **Document library.** 317 entries, with search and filters for board, type and year.

## B. Round-3 content rules followed
- **Town Clerk.** Listed as an office with a phone number and an UNCONFIRMED note. No person is named, and no Town Clerk email appears. Staff are listed by title only.
- **Emails.** Only town role addresses appear, plus the library's info@ address. No personal emails, no home addresses, and the Chamber's email was dropped.
- **Stale and unconfirmed items.**
  - Stale: the Trustees of Trust Funds page (May 2022) and the Energy Commission page are marked "Stale town page".
  - UNCONFIRMED: water and sewer, Town Clerk hours and other unconfirmed items are labeled.
- **Left out entirely:**
  - the "Nov 6, 2026" Planning Board video;
  - trustees' scholarship recipient names;
  - the unverified bridge-approval claim, which is not in the 2026 warrant and was removed from `data.py`.
- **Moved out of the repo.** The stale v1 artifacts `static.html`, `rindge_2026_site_full.html` and `rindge_2026_briefing.pdf` still contained the bridge claim. They are now in `/workspace/rindge_v1_artifacts_outside_repo/`.
- **Budget.**
  - The highway garage bond appears only as "unconfirmed, automated-only".
  - The 497-256 tally appears only as a withheld note.
  - The fiber bond to debt-service link is labeled "Inference, not stated by the town".
  - The 2025 gross appropriations figure of $6,134,500 is marked as an OCR or scan value to verify.
  - The revaluation note says the 2025 and 2024 tax rates are not comparable.
  - 2026 results are labeled Press.
  - Five gaps are listed: debt schedule, 2026 tax rate, multi-year CIP, school budget and FY2027 draft budget.
- **Earlier rules still hold:**
  - the 9/9 ambulance 2-0-1 vote is labeled Press;
  - no audio-derived tallies;
  - no Planning Board 10/6 or joint-budget content beyond agenda listings;
  - none of the forbidden bill or RSA numbers appear;
  - 666-237 is withheld;
  - 2018 Art 13 is unresolved.

## C. Tests (headless Chrome, `test/results_v3.json`)
- **Viewports and motion.** Tested at 375, 768 and 1280 px, with motion on and reduced:
  - 0 console errors and no horizontal overflow;
  - all 232 bar widths match their data;
  - 0 interactive controls under 48 px (618 to 642 checked);
  - bottom nav on phones and tablets, sticky contents rail at 1200 px and wider.
- **Viewer:**
  - open, then Next and Previous;
  - Esc closes, focus returns and the scroll lock is released;
  - focus trap;
  - fallback cards for ext, missing, large and no-PDF-viewer;
  - embeds are sandboxed;
  - Word files show the PDF rendering;
  - the library View button works;
  - 0 document links missing from the registry.
- **Keyboard only:**
  - the first Tab reaches the skip link, which moves focus into main;
  - each of the first 40 Tab stops has a visible focus ring;
  - Ctrl-K opens search: typing, then Enter, goes to the result and opens it, and a document result opens the viewer;
  - Esc closes search;
  - the Display panel opens by keyboard, and text size and theme persist after reload;
  - details open with Enter;
  - deep links open the how-to item they point to.
- **Contrast (WCAG).** Checked on 6,749 text elements in each theme, against their real backgrounds:

  | Theme | AA failures | Lowest ratio | Body text at AAA (7:1) |
  |---|---|---|---|
  | Light | 0 | 5.48 | 100%, lowest 7.49 |
  | Dark | 0 | 6.97 | 100%, lowest 9.22 |
  | High contrast | 0 | 9.35 | 100%, lowest 12.33 |

- **Without JavaScript.** At all three widths, with motion on and reduced: all 18 sections, the 70 timeline entries and the 317 library rows are visible. Charts are drawn at full value, JS-only controls are hidden, and there is no overflow.
- **Private-string scan.** Covers the repo outside the town PDFs, plus the manifest. None of these terms appear: the requester's name or accounts, the private handles, a Town Clerk email, "petition draft", the forbidden bill or RSA numbers, the bridge claim or personal emails. The term "Oeser" appears only in the election results.
- **Screenshots:** `preview.png`, `screenshots/home.png`, `screenshots/viewer.png` and `screenshots/laws.png`.

## D. Size
The repo is about 178 MB: 175 MB of `docs/` and about 3 MB for everything else. `index.html` is 1.15 MB.

---

# Rindge Town Guide v2: audit (Oct 9, 2026, ET)

This adds to the v1 audit below. The build now reads `src/data.py`, `src/v2data.py` (trends, recurring issues, glossary), `src/lawdata.py` (law reference, flows, dimensional table) and `src/v2.py` (renderer). To rebuild, run `python3 src/build.py`. Tests: `node --experimental-websocket test/cdp_test.mjs` (behavior) and `node --experimental-websocket test/sections.mjs` (section screenshots with and without JavaScript).

## A. Method
1. **Sources.** `rindge_annual_reports_by_year.csv` (350 rows) and its notes; the OCR/text of the 2013–2025 annual reports (`/workspace/my/ar/*.txt`); `rindge_multiyear_calendar.md`; `rindge_recurring_issues.md/.csv`; `rindge_local_law_reference.md`; `rindge_state_county_law_reference.md` (including the legal reader's corrections); and press for 2026.
2. **Labels.** Each chart point carries one of these labels: Official; Official · text-extracted · verify against PDF; Official · scan, verify against PDF (rows with ocr_uncertain=yes); Press-reported; Gap; or Withheld. Values the notes call illegible are left out.
3. **Recomputation.** `build.py`/`v2.py` compute every percentage, bar width and stacked segment from raw counts at build time. No hand-entered percentages are used. Tax totals are recomputed as the sum of the printed components and compared with the printed total.
4. **Withheld or unresolved values are left out of the charts.** The 2023 and 2024 budget votes both print 497-256. The 2024 zoning Amendments 4 and 8 (warrant Arts 5 and 9) both print 666-237. 2018 Art 13 is listed as a conflict, not a result.

## B. Number sample re-checked (automated against the CSV): 40 of 40 match
```
MATCH | 2011 budget vote | site=(726, 881) | src=(726, 881) ocr_uncertain=yes label=scan
MATCH | 2011 budget % in HTML | site=True | src=True 45.2%
MATCH | 2012 budget vote | site=(861, 242) | src=(861, 242) ocr_uncertain=yes label=scan
MATCH | 2012 budget % in HTML | site=True | src=True 78.1%
MATCH | 2013 budget vote | site=(558, 381) | src=(558, 381) ocr_uncertain=yes label=scan
MATCH | 2013 budget % in HTML | site=True | src=True 59.4%
MATCH | 2014 budget vote | site=(1229, 211) | src=(1229, 211) ocr_uncertain=yes label=scan
MATCH | 2014 budget % in HTML | site=True | src=True 85.3%
MATCH | 2015 budget vote | site=(1037, 134) | src=(1037, 134) ocr_uncertain=no label=text
MATCH | 2015 budget % in HTML | site=True | src=True 88.6%
MATCH | 2016 budget vote | site=(858, 357) | src=(858, 357) ocr_uncertain=yes label=scan
MATCH | 2016 budget % in HTML | site=True | src=True 70.6%
MATCH | 2017 budget vote | site=(628, 391) | src=(628, 391) ocr_uncertain=no label=text
MATCH | 2017 budget % in HTML | site=True | src=True 61.6%
MATCH | 2018 budget vote | site=(961, 445) | src=(961, 445) ocr_uncertain=no label=text
MATCH | 2018 budget % in HTML | site=True | src=True 68.3%
MATCH | 2019 budget vote | site=(635, 376) | src=(635, 376) ocr_uncertain=yes label=scan
MATCH | 2019 budget % in HTML | site=True | src=True 62.8%
MATCH | 2020 budget vote | site=(867, 433) | src=(867, 433) ocr_uncertain=no label=text
MATCH | 2020 budget % in HTML | site=True | src=True 66.7%
MATCH | 2021 budget vote | site=(535, 620) | src=(535, 620) ocr_uncertain=no label=text
MATCH | 2021 budget % in HTML | site=True | src=True 46.3%
MATCH | 2022 budget vote | site=(600, 399) | src=(600, 399) ocr_uncertain=no label=text
MATCH | 2022 budget % in HTML | site=True | src=True 60.1%
MATCH | 2025 budget vote | site=(783, 850) | src=(783, 850) ocr_uncertain=no label=text
MATCH | 2025 budget % in HTML | site=True | src=True 47.9%
MATCH | 2011 tax total (sum of components) | site=25.32 | src=25.32 printed=25.32
MATCH | 2012 tax total (sum of components) | site=24.63 | src=24.63 printed=24.63
MATCH | 2013 tax total (sum of components) | site=25.46 | src=25.46 printed=25.46
MATCH | 2014 tax total (sum of components) | site=26.03 | src=26.03 printed=26.03
MATCH | 2015 tax total (sum of components) | site=27.89 | src=27.89 printed=27.89
MATCH | 2016 tax total (sum of components) | site=27.91 | src=27.91 printed=27.91
MATCH | 2017 tax total (sum of components) | site=27.19 | src=27.19 printed=27.19
MATCH | 2018 tax total (sum of components) | site=27.5 | src=27.5 printed=27.5
MATCH | 2019 tax total (sum of components) | site=27.76 | src=27.76 printed=27.76
MATCH | 2021 tax total (sum of components) | site=22.65 | src=22.65 printed=22.65
MATCH | 2022 tax total (sum of components) | site=23.03 | src=23.03 printed=23.03
MATCH | 2023 tax total (sum of components) | site=25.04 | src=25.04 printed=25.04
MATCH | 2024 tax total (sum of components) | site=25.31 | src=25.31 printed=25.31
MATCH | 2025 tax total (sum of components) | site=13.79 | src=13.79 printed=13.79
```
Checked by hand against the CSV/MS-1 text, all matching: elderly exemption values for 2011–2015 and 2017–2019 ($8,186,992 … $10,442,080); 2020 (91 recipients, $11,067,758); 2025 (52, $6,559,100); 2016 back lots 439-774; 2022 Art 11 elderly petition 395-601; 2012 Art 20 615-492 (scan); the 3/5 near misses (2011 Art 8 814-785, 2013 Art 7 411-538, 2017 Art 6 567-459, 2019 Art 8 653-409, 2025 Art 11 576-1045); ballots cast for 2011, 2012, 2014, 2016, 2017, 2018 and 2020. The 2021 Art 19 OCR confirms the Deliberative Session amended the article into a study committee (18-6) and that 748-376 is the vote on the amended article.

**Re-checked on the web (Oct 9):**
- HB 1300 (Chapter 324, RSA 32:5-i): the school tax-cap question is on every Nov 3, 2026 ballot and needs 3/5. Confirmed by gc.nh.gov, NHPR (10/1/26) and Citizens Count.
- Ledger-Transcript 9/14/26: Select Board 2-0-1 to move ambulance service to Peterborough from 1/1/2027, about $280,217 per year, subject to voter approval. Labeled Press.
- 2026 budget 707-824 and the 2025/2024 tax rates of $13.79 and $25.31: unchanged from the v1 checks below.

## C. Browser tests (headless Chrome, Oct 9)
- **375 / 768 / 1280 px, with both reduced motion and normal motion:** 0 console errors, 17 charts, 172 bars with 0 bad widths, 0 horizontal overflow. Each chart animates once. The menu works on mobile.
- **Filters:** timeline filters work (70 events). The law filter shows 68 items, County shows 4 and "frontage" finds 8. The theme toggle works.
- **No JavaScript:** all sections render, 116 of 116 bar fills are visible at final width, and the body text matches the JS version within 0.5% (the difference is JS-only controls).
- **preview.png** is refreshed from the 1280 screenshot.

## D. Content safety checks (string scan of index.html)
None of these appear: the requester's name or accounts, a Town Clerk email address, "petition draft", HB 1291, SB 538, RSA 674:33-b, 674:36-a or 72:43-b, police wages.
- Non-public sessions appear only as "contents are not public and are not summarized".
- Planning Board 10/6 appears only as an agenda listing, with the outcome not verified. Nothing comes from the joint budget meeting.
- The highway garage bond appears only as "unconfirmed, automated-only".
- The 9/9 ambulance vote is Press, with no tally taken from audio.
- Audio items name no residents. Petitioners are not named. PB Chair Oeser appears only in the election context.

## E. Unresolved (left visible on the site under Gaps & conflicts)
1. **2023 and 2024 budget votes** both print 497-256. Withheld pending the Town Clerk or ballot PDFs.
2. **2024 zoning Amendments 4 and 8** (warrant Arts 5 and 9) both print 666-237. Withheld.
3. **2018 Art 13** (250th ETF): the typed minutes show a 715-715 tie, a handwritten figure reads 711-707. Unresolved.
4. **2023 town meeting date:** the report says March 14, the ordinance cover says March 28.
5. **2016 Deliberative Session date** conflicts between sources.
6. **Elderly married income limit:** the 2020 MS-1 prints $50K, while the 2025 report and the 2012 Art 20 give $49K.
7. **2025 default budget:** the official $5,487,882 differs from press figures.
8. **Revaluation increase:** 89.6% (town page, residential) vs 96.7% (other source).
9. **March 2026 results,** including the ADU article 1,130-526, are press-only until the 2026 annual report is out.
10. **Ballots cast 2021–2026 and elderly values 2016 and 2021–2024** were not found or not extracted, so they are shown as Gap. The 2013 figure (966) is "voters at second session".
11. **Online archive starts Sept 2024.** Earlier "first found" dates are upper bounds; older minutes need a records request to the Executive Secretary/Town Administrator.
12. **Scan-only values** (2011–2014, 2016, 2018 and 2019 ballot pages) need checking against the PDFs before anyone quotes them.
13. **2027 petition and zoning dates** are derived from statute and have not been confirmed by the town.

---

# Rindge 2026 site: accuracy audit and polish pass (Oct 9, 2026, ET)

The final file is `index.html`, a single self-contained page with no external requests. It is generated by `src/build.py` from `src/data.py`, `src/template.html`, `src/style.css`, `src/app.js` and `meetings.json`. To rebuild, run `python3 src/build.py`. Browser tests are in `test/cdp_test.mjs` (run with `node --experimental-websocket test/cdp_test.mjs`).

## 1. What I checked

### Re-verified online on Oct 9

| Item | Value on site | Verified against | Result |
|---|---|---|---|
| 2026 operating budget vote | 707 yes, 824 no (46.2% yes) | Ledger-Transcript 3/11/26; Keene Sentinel 3/10/26 | Match |
| Select Board race | Hamilton 832, Martin 661 | Both articles | Match |
| Planning Board race | Aho 684, Helsel 683, Oeser 671, Hower 508 | Ledger-Transcript | Match (added; new) |
| Stay with SB2 | 278-197 | Keene Sentinel | Match |
| Voting machines | No 283, Yes 198 | Keene Sentinel | Match |
| Hand count | 270-207 | Keene Sentinel | Match |
| Art. 15 "Protect the Taxpayer" (petition) | 1,041-486 | Ledger-Transcript | Match |
| Art. 16 rescind ninth officer (petition) | 914-619 | Ledger-Transcript | Match |
| CRF/ETF articles | 1,004-526; 1,082-446; 1,307-230; 1,060-465; 1,095-438; 996-535; 1,171-361 | Ledger-Transcript | Match |
| Deliberative Session | $40K amendment unanimous; $100K police amendment 85-50; final $5.81M; LUCT amended 20% to 99% | Ledger-Transcript 1/31/26 | Match. Corrected the old "+$140K, 85-50" wording: 85-50 applied only to the $100K amendment. |
| 2025 / 2024 tax rate | $13.79 / $25.31 | Town Tax Collector page | Match |
| 2025 components | Town 2.44, county 2.01, state 0.98, local 8.36; commitment $19,904,756 | NH DRA 2025 rate table (search snippet; direct PDF download returned 403) and the Annual Report | Match |
| 2021–2024 components | See chart | 2025 Annual Report "Tax Rate Comparison" table (web search snippet plus local copy of the report) | Match. The 2024 breakdown was previously "not in sources"; it is now charted. |
| 2025 shares | Local 60.6%, town 17.7%, county 14.6%, state 7.1% | Annual Report pie chart; recomputed from values | Match |
| Revaluation | +89.6% average residential | Town "Calculating Tax Impact for 2025" page | Match |
| Population | 6,476 (2020 Census); 6,502 (July 1, 2025 est.) | Census QuickFacts | Match |

### Checked against the 2025 Annual Report (official; local text copy of the posted PDF)

- **Elderly exemption.** $100K / $140K / $200K; 20 / 13 / 19 recipients; per-tier totals $1,876,600 / $1,726,500 / $2,956,000, summing to $6,559,100. Income limits $35K / $49K; asset limits $150K / $150K. The disabled exemption uses the same limits. All match. The online assessing form URL now returns 404, so I used the Annual Report instead.
- **2025 Art. 15 Revaluation CRF.** $25,000, passed 872-736. Added.
- **2026 default budget.** $5,654,177. Added as the official figure; press figures ($5.64M, $5.65M, $5.7M) are noted as a conflict.
- **Final 2026 warrant numbering.** Art. 4 Highway CRF $185K, 5 Fire $125K, 6 Ambulance ETF $40K, 7 Building $35K, 8 Recreation $25K, 9 Meetinghouse $25K, 10 Library $20K, 11 250th, 12 Veterans credit, 13 Farm structure, 14 LUCT, 15 and 16 petitions. The old page listed the Jan 7 draft values as if they were the final warrant; this is fixed.
- **Exemption filing deadline.** April 15, 2026, from the town calendar in the report.

### Checked against the source files

`rindge_2026_calendar.md`, `rindge_2026_board_decisions.md`, `rindge_recordings_report.md`, `rindge_legal_findings.md`, `rindge_reval_articles.md`, `rindge_agenda_table.md`, `rindge_board_findings.md`. I re-read every timeline note and topic fact against them.

- The Revaluation CRF on the Jan 7 draft was pulled Jan 21 (BOS 1/21 minutes quote). Added.
- The LUCT article was amended from 20% to 99%. The old page said 20%. Fixed.
- The veterans' credit is Art. 12 on the final warrant (Art. 11 in the draft). Fixed and noted.
- ZBA 9/22 Case 2026-12 (4-1) is labeled "draft minutes". ConCom 7/23 $2,500 to LEC Environmental Consultants (5-0-1) is official. The consultant's personal name was removed.

### Chart math

All 38 chart bars were recomputed in `build.py` from the raw counts, not typed in by hand.

- **Yes/no charts:** each bar is its share of (yes + no). For example, 707 / 1,531 = 46.18%.
- **Candidate races:** bars are scaled to the top vote-getter, and this is stated on each chart.
- **Tax chart:** a common $0–$30 axis, with ticks at 0 / 10 / 20 / 30 aligned to the gridlines at 33.3% intervals. The totals are sums of the components.

## 2. Browser tests

Headless Chrome via the DevTools protocol, at 375×812, 768×1024 and 1280×900. Each width was run with normal motion and with `prefers-reduced-motion: reduce`.

- Zero console errors, warnings or exceptions in all 6 runs.
- All 38 bars ended within 0.5% of their target width in every run.
- **Animation:** bars are 0 width before scrolling and animate once on scroll into view. The class is added at most once per chart; scrolling away and back does not re-run it.
- **Reduced motion:** final values are shown immediately at load.
- **Without JavaScript:** a script-stripped copy renders the full page (timeline, key dates, charts at final values, tables, topics as native `<details>`). Filter controls are hidden.
- **Filters:** a board chip, All boards, search ("forristall" returns 3 entries), the source filter (official 66, unofficial 5) and the minutes filter all work. The result count is announced (`aria-live`).
- **Navigation and theme:** the mobile menu opens and closes, with `aria-expanded` and Escape to close. The theme toggle, back-to-top and scroll progress bar work.
- **Layout:** no horizontal overflow at any width.

## 3. What I changed

### Rules for a public page

- Every item from the 9/9, 9/23 and 10/7 Select Board audio is labeled "Unofficial, from meeting audio · approximate until minutes are posted".
- No tallies appear after the approved-minutes cutoffs (Select Board 8/12, Planning Board 8/4, Conservation Commission 8/10). The only exceptions are the BS&A renewal (3-0) and the 10/7 rehearing request (3-0), both labeled as audio.
- The 9/9 ambulance vote shows no tally.
- Removed:
  - The 9/1 PB "waivers denied 5-0".
  - The 10/7 EOP "3-0".
  - The school board "7-0".
  - The joint BAC "unanimous agenda".
- Nothing is published from the Planning Board 10/6 recording or summary, or from the joint budget meeting. Both are listed only as gaps; the PB 10/6 entry is agenda-only.
- Automated-only claims are labeled "Automated summary · unconfirmed" or removed. The ConCom "opposes 75 ft" claim, the December hearing, the highway garage bond and the school items are caveated.
- No names of residents are tied to AI summaries or audio. Removed:
  - The Energy Commission appointee's name.
  - Named public commenters.
  - The superintendent's name, which came from an automated summary.
  - The consultant's personal name.
  - The ZBA applicants' personal names and home addresses (a developer or LLC name is kept where it identifies the case).
- Non-public session content (including wages) is excluded. Non-public entries say only that the contents are not summarized.
- Removed the Boardwalk Regional Impact 4-3 vote.
- Removed private or pending research content:
  - The draft elderly-exemption petition checklist.
  - The letter-writer's stated plan.
  - Any reference to a specific person's petition or email.
  - The planning director's direct extension.
- Kept the current exemption limits and the general petition law, labeled "summary, not legal advice" with source links.
- **Date labels:**
  - "Unofficial / inferred": Select Board 10/21, 11/4, 11/18; Planning Board 11/3, 11/17, 12/1; ZBA 11/24; Deliberative Session Jan 30, 2027.
  - "Statutory, not confirmed by the town": Jan 12, 2027.
  - "Derived from statute / NHMA calendar, not posted by the town": the other SB2 dates.
  - No video links are promised for future meetings.
- Added:
  - A top notice: "Unofficial community research. Not affiliated with or endorsed by the Town of Rindge."
  - "Last updated Oct 9, 2026" in the notice bar and the footer.
  - A "Report a correction" footer pointing to the Planning Department and Town Clerk at the Town Offices' main number. No personal email.

### Content updates

- New 5-year tax-rate chart with a data table.
- New Planning Board race and petition-article charts.
- Capital reserve results table.
- Revaluation facts: 2025 Art. 15 passed 872-736; the 2026 draft article was pulled Jan 21.
- Conflicts list updated:
  - Default budget figure.
  - Draft vs. final warrant.
  - Forristall Rd rehearing vs. the 4-1 grant.
  - Election results source.
  - Removed internal-notes references and named-person conflicts.

### Polish

- Town-appropriate palette (forest green, granite, maple accent) with a matched dark theme.
- System serif/sans type pairing and consistent card spacing.
- Skip link, `:focus-visible` states, aria labels on charts (`role="img"` with the full value text), `aria-pressed` on chips, `aria-current` in the nav, labeled form fields, and `<time>` elements.
- Badge colors chosen for readable text contrast in both themes.
- Mobile hamburger menu (without JS, the nav wraps instead).
- Back-to-top button and scroll progress bar.
- Print stylesheet: hides the chrome, expands all topics, prints link URLs and shows bars at full value.
- Reduced-motion fallback.
- Static HTML for every section, so the page is not blank without JS.

## 4. Items I could not verify

- The town's official 2026 election results page (`news_detail_T2_R44.php`) returned 404, so all 2026 tallies are press-reported. The SB2, voting-machine and hand-count totals (~475 votes) are far below the ~1,530 on other questions; this is shown as reported and flagged. Tallies for 2026 Arts. 12–14 were not found.
- NH DRA tax-rate PDFs returned 403 to direct download; values were confirmed via the DRA search snippet and the town's Annual Report.
- Every board-minutes tally is from text extraction; individual PDFs were not re-opened in this pass. Each one carries a "verify against the PDF" badge.
- The Select Board 9/9, 9/23 and 10/7 items are machine speech-to-text; amounts and outcomes are approximate until minutes are posted.
- No official record exists yet of the 10/7 rehearing request, the Peterborough contract terms, or the ConCom position on 75 ft.
- School district items were not checked against district minutes.
- The Wetlands ordinance file is dated 2023; later amendments were not confirmed.
- Article 14 in the ConCom 2/26 minutes is identified as the LUCT article by matching the BAC 5-2 recommendation on the final warrant. This is an inference, consistent with the warrant.

## v4 redesign (Oct 10, 2026) — local build, not published

Navigation and layout
- One navigation pattern: slim translucent sticky top bar (site name, Search, Menu). Menu is a full-screen sheet on phones and a right-hand sheet on tablets/desktop, grouped into plain-language categories. At 1280 px and wider the same bar also shows six top-level links. The old sidebar is gone.
- Home is a "Start here" page: six task cards (What happened this year?, When is the next meeting?, Find a document, How do I...?, Who do I call?, Taxes and exemptions), a search box, and more questions.
- Every section has breadcrumbs (Home / group / section), a one-sentence summary and a "In plain language" card. Back-to-top button, skip link, focus rings, logical headings (h1 > h2 > h3).
- Apple-style system font, strict type scale (body >= 17 px, fluid with clamp()), one accent colour, large-radius cards, blurred bars, 8 pt spacing, 150–250 ms motion, reduced-motion and dark/high-contrast themes, safe-area insets, 100dvh sheets, scroll-padding under the bar.

Expandable cards (accordion in place)
- 229 cards expand in place: 70 meetings, 24 key dates/meeting rows, 12 recurring issues, 77 laws, 34 directory entries, 12 stat cards. Each has a visible "Details" button with chevron and a short summary of what is inside, aria-expanded/aria-controls, Enter/Space, Esc to close (focus returns to the button), tap anywhere on the card, smooth 220 ms height animation (none with reduced motion), and a deep link (#card-id opens it; opening a card updates the address).
- Details show the full record: all notes and vote tallies with their source badges, documents and video, and links. Calendar rows link to the meeting record, the board's regular details, and related rules and guides already on the site. Stat cards list where to check the number (sources already cited on the site) and where to see more.
- Cards that have nothing more to show are not styled as clickable. Without JavaScript every card shows everything.

Documents and video inside the site
- PDFs (156) and converted Word files (6) render inside the full-screen viewer with the bundled PDF.js 4.10.38 (vendor/pdfjs, Apache-2.0): page number box, previous/next page, zoom out/in, fit width, Download, Open original, Close, previous/next document. A loading spinner shows until the first page is drawn; if a file cannot be drawn, the sheet shows Open/Download/Original buttons instead of a blank frame. Large scans (3) and missing files (2) show an explanation card; outside pages that refuse framing (113) open in a new tab; outside pages that allow framing (14) show in the sheet with a loading state.
- Town Hall Streams refuses to be framed (X-Frame-Options: SAMEORIGIN), so the 23 Select Board meeting videos play from its public HLS stream (CORS allowed) in the site's own player: native HLS where available, hls.js 1.7.3 (vendor/hls, Apache-2.0) elsewhere. Poster card first; one automatic retry; then a clear "Watch on Town Hall Streams" fallback.
- For the three meetings this guide transcribed (Sept 9, Sept 23, Oct 7, 2026), the sheet lists topic jump links (timestamps from rindge_recordings_report.md) with short excerpts copied verbatim from /workspace/rec/*.txt (checked by src/curate_excerpts.py). Labeled "Unofficial · own transcription"; the note says they come from automatic speech-to-text of the audio, were not checked against the video, and may be wrong. Excerpts avoid personal remarks and obvious mis-hearings; the full transcripts are not published.

Content
- No facts added. The elderly exemption count is stated as 91 (2020), 92 (2021), 89 (2022), 88 (2023), 44 (2024), 52 (2025), and the drop followed the 2024 assessor review.
- Exclusions kept: no Town Clerk email, no exemption petition, no family information. Site stays labeled unofficial and not affiliated with the Town. Unconfirmed-date labels kept (Jan 12, 2027 petition deadline; March 2027 ordinance hearing).

Exports
- static.html (no JavaScript, everything expanded) and rindge_2026_briefing.pdf (printed from it) regenerated in the site folder by src/export_static.py. The stale v1 copies in /workspace/rindge_v1_artifacts_outside_repo/ were left untouched.

Tests: test/cdp_test.mjs (headless Chrome over CDP, served over local HTTP like GitHub Pages) -> test/results_v4.json and test/shots_v4/.
