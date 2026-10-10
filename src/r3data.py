# Round 3 content: directory, how-do-I guides, budget, schools/community, emergency/utilities, facts/history.
# Sources: rindge_town_directory.md, rindge_public_info.md, rindge_how_do_i_guides.md, rindge_budget_finance.md/.csv (all checked Oct 9, 2026).
# Rules: offices by title only (no staff names); town role addresses only (no personal emails, no Town Clerk email);
# UNCONFIRMED and stale items labeled; no "Nov 6, 2026" Planning Board video; no unverified bridge-approval claim; no 2024 497-256 tally.
G = "https://www.rindgenh.gov/"
O = "https://www.rindgenh.org/"
AR25 = "https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/0%202025%20Annual%20Report%20for%20the%20Town%20of%20Rindge.pdf"
AR24 = "https://www.rindgenh.org/Documents/How%20Do%20I/Town%20Reports/2024%20Annual%20Report-Town%20of%20Rindge-Final%20Print.pdf"
ZO = "https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Zoning%20Ordinances/Zoning_Ordinance%20Amended%20March%2011,%202025.pdf"

TOWN = dict(addr="Town Offices, 30 Payson Hill Road, Rindge, NH 03461", phone="(603) 899-5181", fax="(603) 899-2101",
            hours="Hours vary by office (see each office below).", url=G + "how_do_i/contact_us.php")

# (office, what it does, phone, email or "", hours, address, url, labels, note)
DEPTS = [
 ("Town Clerk's office", "Vehicle registrations, dog licenses, vital records, marriage licenses, elections and voter registration, transfer station stickers.",
  "(603) 899-5181 x107", "", "Mon 8–1 and 1:30–4; Tue noon–6:30; Wed 8–1 and 1:30–4; Thu 7–1 and 1:30–3:30; Friday not listed (appears closed, unconfirmed).",
  "Town Offices", G + "departments/town_clerk/index.php", ("role",),
  "The town's pages name different people for this office, so this guide lists the office only until the town confirms (UNCONFIRMED). Online vehicle renewals: E-Reg."),
 ("Tax Collector", "Property tax bills (about July 1 and Dec 1), payments. Cash or check only; bills are not online.",
  "(603) 899-5181 x108", "", "Mon–Thu 9–1 and 2–4; Fri closed.", "Town Offices (mail: P.O. Box 11, Rindge, NH 03461)", G + "departments/tax_collector/index.php", ("role",),
  "2026 first-half bills were mailed May 26 and due July 1, 2026. Tax year runs April 1 to March 31."),
 ("Assessing", "Property values, exemptions and credits, abatements, current use. The Select Board acts as the Board of Assessors.",
  "(603) 899-5181 x113", "", "Wed and Thu 12:30–4:30 (temporary change posted for Oct 5–8, 2026).", "Town Offices", G + "departments/assessing/index.php", ("role",),
  "Abatement applications are due March 1; exemption and credit applications April 15."),
 ("Building Department", "Building, electrical, plumbing and mechanical permits; inspections; certificates of occupancy.",
  "(603) 899-5181 x109 · inspections line (603) 969-3354 (call or text)", "buildingdept@rindgenh.gov", "Office Mon–Thu 1–3. Inspections Mon–Thu 8–10 am; request 24 hours ahead by phone, not email. Applications reviewed Wednesdays 10 am.",
  "Town Offices", G + "departments/building/index.php", ("role",), ""),
 ("Planning Department", "Subdivision, site plan, conditional use, zoning questions, Planning Board support, Master Plan.",
  "(603) 899-5181 x117 (call ahead)", "", "Mon–Wed 9–4; Thu by appointment.", "Town Offices", G + "boards_commission/planning_board/index.php", ("role",),
  "Applications are due 21 days before the hearing. A pre-application meeting is recommended."),
 ("Zoning / Code Enforcement", "Complaints about zoning, wetlands and signs.", "(603) 899-5181 x115", "", "Not posted (gap).", "Town Offices",
  G + "departments/code_enforcement/index.php", ("role",), ""),
 ("Select Board office / Town Administrator", "Board agendas, town administration, records requests. Agenda requests go to the Town Administrator by noon Thursday before a meeting.",
  "(603) 899-5181 x101 (Town Administrator) · x100 (Executive Secretary)", "townadmin@rindgenh.gov · executivesecretary@rindgenh.gov", "Mon–Thu 9–4; Fri closed.",
  "Town Offices", G + "boards_commission/board_of_selectmen/index.php", ("role",),
  "Older minutes (before about 2024) are available by records request to the Executive Secretary or Town Administrator."),
 ("Public Works (Highway)", "Roads, plowing, culverts, paving. Maintains 64 miles of Class V road (55 paved, 9 gravel).", "(603) 899-2105", "",
  "Mon–Thu Nov–Apr 7:00–3:30, May–Oct 6:00–4:30; Fri Nov–Apr 7:00–3:30.", "115 Main Street (mail to Town Offices)", G + "departments/public_works/index.php", ("role",),
  "The 2025 Annual Report's highway report says 65 miles; the department page says 64."),
 ("Recycling and Transfer Station", "Trash and recycling drop-off, Swap Shop.", "(603) 899-2105", "", "Tue 10–7, Thu 10–7, Fri 1–7, Sat 8–3. Swap Shop Tue 10–2, Sat 9–2.",
  "113 Main Street", G + "departments/recycling_transfer_station/index.php", ("role",),
  "Stickers (Apr 16, 2026–Apr 15, 2027): $50, or $25 for one senior (65+) per household. Sold at the Town Clerk's or Selectmen's office, not at the station."),
 ("Fire Department and Emergency Management", "Fire, rescue, fire prevention, emergency management, burn-permit questions.", "(603) 899-3324 · emergencies 911",
  "rfdchief@rindgenh.gov · rfdprevention@rindgenh.gov", "Not posted (gap).", "150 Main Street", G + "departments/fire/index.php", ("role",), "Residential trash burning is prohibited."),
 ("Police Department", "Police services, records requests, pistol permits, property checks, police logs.", "(603) 899-5009 · after hours (603) 355-2000 · emergencies 911", "",
  "Mon–Fri 8–4.", "158 Main Street (P.O. Box 7)", G + "departments/police/index.php", ("role",), ""),
 ("Health Officer", "Public health complaints and inspections.", "(603) 899-5181 x100", "", "Not posted (gap).", "Town Offices", G + "departments/health_officer/index.php", ("role",), ""),
 ("Ingalls Memorial Library", "Books, e-books, Wi-Fi, computers, printing, children's programs. No public meeting room.", "(603) 899-3303", "info@ingallslibrary.com",
  "Mon 10–5, Tue 1–8, Wed 10–5, Thu 1–8, Fri 10–5, Sat 9–12.", "203 Main Street (P.O. Box 224)", G + "departments/ingalls_memorial_library/index.php", ("role",), "Library website: ingallslibrary.com."),
 ("Recreation Department", "Programs, camps, Rec Building and pavilion rentals.", "(603) 899-6847", "recdirector@rindgenh.gov", "Not posted (gap).",
  "Wellington Park, 283 Wellington Road", G + "departments/recreation/index.php", ("role",), "Online registration: rindge.recdesk.com."),
 ("Welfare (General Assistance)", "Temporary help with basic needs, paid to vendors. Apply monthly.", "(603) 899-5181 x112", "welfare@rindgenh.gov", "Not posted (gap).",
  "Town Offices", G + "departments/welfare/index.php", ("role",), ""),
 ("Cemetery Trustees and Sexton", "Hillside Cemetery (Goddard Road): lots and burials.", "(603) 899-5181 x100 · Sexton (603) 899-2105", "", "Trustees meet the 4th Thursday, 3 pm, Town Offices.",
  "Town Offices", G + "boards_commission/cemetery_trustees/index.php", ("role",), ""),
]

# (board, schedule, contact, url, labels, note)
BOARDS3 = [
 ("Select Board (3 members)", "Usually every other Wednesday, 6 pm, Conference Room, Town Offices. Streamed on Town Hall Streams.", "(603) 899-5181 x101", G + "boards_commission/board_of_selectmen/index.php", ("role",),
  "Approved minutes posted through Aug 12, 2026; none yet for Aug 26, Sept 9, Sept 23 or Oct 7."),
 ("Planning Board", "1st and 3rd Tuesday, 7 pm (first meeting hears applications; second is a work meeting).", "(603) 899-5181 x117", G + "boards_commission/planning_board/index.php", ("role",),
  "Chair not listed on the town page (gap). Draft minutes are available at the Town Office within 144 hours; the website posts approved minutes. The town site lists no Planning Board video links."),
 ("Zoning Board of Adjustment", "4th Tuesday, 7 pm, Conference Room.", "(603) 899-5181 x105 · ZoningClerk@rindgenh.gov", G + "boards_commission/zoning_board_of_adjustment/index.php", ("role",), ""),
 ("Conservation Commission", "2nd Monday and 4th Thursday, 6:30 pm (except Nov and Dec) or as posted.", "(603) 899-5181 x100 · rindgeconcom@rindgenh.gov", G + "boards_commission/conservation_commission/index.php", ("role",), ""),
 ("Budget Advisory Committee (RSA 32:24)", "Schedule not posted (see agendas page).", "(603) 899-5181", G + "boards_commission/budget_advisory_committee/index.php", ("role",), ""),
 ("Capital Improvement Program Committee", "Meets in the fall to prepare capital recommendations (projects of $10,000 or more). Schedule not posted.", "(603) 899-5181 x117", G + "boards_commission/capital_improvement_program_committee/index.php", ("role",), ""),
 ("Trustees of the Trust Funds", "Page lists a meeting date of May 9, 2022 only. Recent minutes: Nov 18, 2024 and May 13, 2025.", "trusteetrustfunds@rindgenh.org", G + "boards_commission/trustees_of_trust_funds/index.php", ("stale",), ""),
 ("Energy Commission", "3rd Friday, 4 pm. Latest posted minutes: Sept 12, 2024.", "(603) 899-5181", G + "boards_commission/energy_commission/index.php", ("stale",), ""),
 ("Community Power Committee", "Formed by the Select Board Nov 1, 2023. Schedule not posted.", "(603) 899-5181", G + "boards_commission/community_power_committee/index.php", ("role",), ""),
 ("Recreation Committee", "Alternates 1st Monday / Wednesday monthly. Agenda items in writing one week ahead to the Recreation Director.", "(603) 899-6847", G + "boards_commission/recreation_committee/index.php", ("role",), ""),
 ("Roadway Committee", "Recent meetings June 9 and July 9, 2026.", "(603) 899-5181", G + "boards_commission/roadway_committee/index.php", ("role",), ""),
 ("Hazard Mitigation Committee", "Schedule not posted.", "(603) 899-3324", G + "boards_commission/hazard_mitigation_committee/index.php", ("role",), ""),
 ("Meetinghouse Oversight Committee", "Oversees the Meeting House, 6 Payson Hill Road. Schedule not posted.", "(603) 899-5181", G + "boards_commission/meetinghouse_oversight_committee/index.php", ("role",), ""),
 ("Supervisors of the Checklist", "Voter checklist. Session before the Nov 3, 2026 election: Wed Oct 28 (time posted by Oct 15).", "Town Clerk's office (603) 899-5181 x107", G + "boards_commission/supervisors_of_the_checklist/index.php", ("role",), ""),
 ("Teltech Committee", "Town telecommunications/broadband committee (purpose not stated on page). Schedule not posted.", "(603) 899-5181", G + "boards_commission/teltech/index.php", ("role",), ""),
 ("Town & Gown Committee", "3rd Tuesday, 2 pm, alternating Town Office and Franklin Pierce University.", "(603) 899-5181", G + "boards_commission/town_gown_committee/index.php", ("role",), ""),
 ("Agriculture Committee", "Listed in the town directory; no page found.", "(603) 899-5181", G + "how_do_i/contact_us.php", ("gap",), ""),
 ("Ambulance Services Committee", "No town page found. A May 12, 2026 meeting appears on Town Hall Streams.", "(603) 899-5181", "https://townhallstreams.com/towns/rindge_nh", ("gap",), ""),
]

ONLINE = [
 ("Pay bills online", "https://pay.eb2gov.com/RINDGENH"), ("Renew a vehicle registration (E-Reg)", "https://pay.eb2gov.com/Service/Index/1422?towncode=328&source=MV&towncodemasterid=321"),
 ("Recreation registration", "https://rindge.recdesk.com/Community/Home"), ("Email notices (eNotify)", G + "enotify/index.php"),
 ("Citizen Request Center (web form)", G + "boards_commission/board_of_selectmen/citizen_request_center.php"), ("Assessing database", "https://data.avitarassociates.com/logon.aspx"),
 ("Watch Select Board meetings (Town Hall Streams)", "https://townhallstreams.com/towns/rindge_nh"), ("Town calendar", G + "calendar.php"),
]

DIR_GAPS = [
 "Who holds the Town Clerk position: town pages disagree. This guide names the office only (UNCONFIRMED).",
 "Email addresses for the Tax Collector, Assessing, Public Works, Planning and Code Enforcement: sources disagree or none is listed. Call the office.",
 "Hours for Fire, Recreation, Welfare and Code Enforcement are not posted. Friday hours for the Town Clerk's office are not listed.",
 "Planning Board chair, and an official video source for Planning Board, ZBA and Conservation Commission meetings: not on the town site. Third-party video titles are unverified.",
 "Meeting schedules for the Budget Advisory, CIP, Community Power, Hazard Mitigation, Meetinghouse, Supervisors and Teltech committees; the Trustees of the Trust Funds page is stale (May 2022).",
 "Whether a Heritage Commission, Agriculture Committee page or Ambulance Services Committee page exists.",
]

# ---- How do I...? (q, plain steps list, details list [(label, text)], who, legal, labels, links [(text,url)], gaps)
FEES = "https://www.rindgenh.org/Documents/Departments/Building/Files%20Documents/2026%20Official%20Building%20and%20Fire%20Department%20Permit%20Fee%20Schedule.pdf"
GUIDES = [
 ("get a building permit?", "building",
  ["Check zoning first: district, setbacks, frontage and wetlands. For anything beyond a simple house, call Planning (x117). A permit is required before any building goes up (Zoning Art. III.A).",
   "Get the right form from the Building Department documents page. Attach plans and pay the fee with the application; inspections are not scheduled until payment is in.",
   "Applications are reviewed every Wednesday at 10 am.",
   "Request each inspection at least 24 hours ahead by phone or text to (603) 969-3354. Do not request inspections by email.",
   "Get a certificate of occupancy before moving in or changing use, including seasonal to year-round (Zoning Art. III.C)."],
  [("Fees (2026 schedule, scanned; verify before quoting)", "Minimum $60. New one- or two-family home $0.40 per sq ft of living area; basements, garages, decks and porches $0.25 per sq ft. Additions $0.40 per sq ft. Demolition $65. Pools $60. Starting work without a permit doubles the fee, and violations can cost $100 a day."),
   ("Single-family homes", "Single-family homes and duplexes do not need Planning Board site plan review.")],
  "Building Department, (603) 899-5181 x109, buildingdept@rindgenh.gov.", "Zoning Ordinance Art. III.A and III.C; NH State Building Code (RSA 155-A).", ("official", "scan"),
  [("Building forms page", G + "departments/building/files_documents.php"), ("2026 permit fee schedule", FEES), ("Zoning Ordinance", ZO)],
  ["The fee schedule says permits are valid 1 year in one place and 180 days in another. Ask the Building Department.", "No online permit portal was found (unconfirmed)."]),
 ("get a driveway permit?", "road",
  ["Get the Residential (or Commercial) Driveway Access Permit Application from the Planning Board applications page.",
   "Check the Driveway Regulations: residential driveways 10–20 ft wide; sight distance by road speed (150 ft at 25 mph up to 400 ft at 60 mph); runoff must not enter the road.",
   "Attach a sketch plan. A rough drawing is accepted.",
   "Pay two checks to the Town of Rindge: a $50 application fee and a $500 security bond, which may be returned once the driveway passes.",
   "Public Works inspects before approval and before construction starts."],
  [("Class VI or private road", "Building on a Class VI or private road needs a Class VI Road Waiver (RSA 674:41). The fee is $50 total, in two checks: $12.78 to the Cheshire County Registry of Deeds and $37.22 to the Town.")],
  "Planning Department (x117); inspection by Public Works.", "RSA 236:13; Zoning Art. III.A.2; Driveway Regulations (amended Dec 5, 2017).", ("official",),
  [("Planning Board applications", G + "boards_commission/planning_board/applications.php"),
   ("Driveway Regulations", "https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Regulations/driveway_regulations_amended_december_5_2017.pdf")],
  ["The form is dated 2012. Ask Planning whether the $50 and $500 amounts are current.", "State highways need a NH DOT driveway permit (not researched)."]),
 ("put in a septic system or work near wetlands?", "water",
  ["A licensed NH septic designer prepares the plan. NH DES must approve construction before you build, and approve operation before use.",
   "Rindge's Wetlands Conservation District Ordinance: a new septic tank or leach field must be at least 100 ft from surface waters and vegetated wetlands; septic piping at least 50 ft. No building or pavement within 50 ft. No fertilizer (other than limestone) within 25 ft.",
   "Work in wetlands or streams usually needs a NH DES wetlands permit. Land within 250 ft of public waters is protected shoreland.",
   "Talk to the Planning Department early. The Conservation Commission gets notice of applications affecting the wetlands district."],
  [("Pending change", "The Planning Board has discussed changing the septic setback from 100 ft to 75 ft for the March 2027 ballot. No amendment text was posted as of Oct 9, 2026, so 100 ft is the rule today.")],
  "NH DES, (603) 271-3503; locally Planning (x117) and Code Enforcement (x115).", "RSA 482-A, 483-B, 485-A; Rindge Wetlands Ordinance.", ("official",),
  [("Wetlands Ordinance (amended March 28, 2023)", "https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Zoning%20Ordinances/wetlands_conservation_district_ordinance_amended_march_28_2023.pdf"),
   ("NH DES septic systems", "https://www.des.nh.gov/land/septic-systems"), ("NH DES wetlands permit help", "https://www.des.nh.gov/water/wetlands/permit-assistance")],
  ["Ordinance date conflict: the Annual Report says the vote was March 14, 2023; the ordinance cover says March 28, 2023.", "DES fees were not collected."]),
 ("rent my home short-term (under 30 days)?", "home",
  ["Short-term rentals need Site Plan approval and a Conditional Use Permit from the Planning Board.",
   "Applications are due at the Planning Department at least 21 days before the hearing. The Board hears applications at its first meeting of the month.",
   "The Board looks at septic, water, parking, occupancy (up to 3 people per bedroom) and life-safety inspections."],
  [("When adopted", "March 11, 2025, 881-717 (Zoning Art. III.S and Art. XII).")],
  "Planning Department (x117).", "Zoning Ordinance Art. III.S and XII; RSA 674:21.", ("official",),
  [("Planning Board applications", G + "boards_commission/planning_board/applications.php"), ("Zoning Ordinance", ZO)],
  ["Application fees were not extracted.", "No separate STR registration or fee was found."]),
 ("add an accessory dwelling unit (ADU)?", "home",
  ["One ADU per lot, attached or detached, in the Residential, Residential-Agricultural, Village and College districts, and on legal non-conforming single-family lots elsewhere.",
   "The owner lives in either unit. Size: at least 300 sq ft; at most 950 sq ft (or one-third of a larger home). Two exits, interconnected fire alarms, parking, and a septic system certified adequate.",
   "Get a building permit; plans must show the ADU area. There is no separate ADU form."],
  [("State law", "RSA 674:71–73 limits what towns can require. A town may require owner occupancy of one unit but cannot say which.")],
  "Building Department (permit); Planning (x117) for questions.", "Rindge ADU Ordinance (2026); RSA 674:71–73.", ("official",),
  [("ADU Ordinance (2026)", "https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Zoning%20Ordinances/Accessory%20Dwelling%20Unit%20Ordinance%202026.pdf")],
  ["The 2026 state amendment (effective Aug 31, 2026) was not compared line by line with the town ordinance. Confirm with Planning."]),
 ("put up a sign?", "sign",
  ["Most signs need a permit before they go up or change. Some temporary, charitable and construction signs are exempt but must still meet district rules.",
   "Apply to the Select Board or its designee with location, size, lighting, materials and a drawing, signed by the business and property owners.",
   "Permits carry an annual renewal fee due April 30."],
  [], "Select Board office; enforcement by Code Enforcement (x115).", "Sign Ordinance (amended March 12, 2024).", ("official",),
  [("Sign Ordinance", "https://www.rindgenh.org/Documents/Boards%20Commission/Planning%20Board/Zoning%20Ordinances/sign_ordinance_amended_march_12_2024.pdf")],
  ["No sign permit form or fee amount was found on the website."]),
 ("get a burn permit?", "fire",
  ["New Hampshire requires a written fire permit for open burning unless the ground is snow-covered. Ask the Rindge Fire Department.",
   "Allowed: untreated wood and brush up to 5 inches across. Not allowed: household trash, construction debris, treated wood.",
   "Check fire danger the same day."],
  [("Penalty (2026 fee schedule, scanned)", "Unauthorized burning can bring a state warning and a $350 town fee.")],
  "Fire Department, (603) 899-3324, rfdchief@rindgenh.gov.", "RSA 227-L; Res 5600; Env-A 1000.", ("official", "scan"),
  [("NH Forest Protection: fire permits", "https://www.nhdfl.dncr.nh.gov/forest-protection/fire-permits")],
  ["Rindge's local permit hours and process are not posted. Whether Rindge uses NHFirePermit.com is unconfirmed (the site returned an error)."]),
 ("license my dog?", "dog",
  ["License every dog with the Town Clerk's office by April 30 each year. New tags go on sale in January.",
   "Renew online through the town's online payments if not late, or in person at the Town Offices.",
   "Bring proof of rabies vaccination (confirm with the office)."],
  [("Fees", "$7.50 spayed or neutered; $10.00 not; $2.00 for one dog owned by a senior (65+); $20.00 group license for 5 or more dogs.")],
  "Town Clerk's office, (603) 899-5181 x107.", "RSA 466 (not fetched; the town page is the source).", ("official",),
  [("Town Clerk page", G + "departments/town_clerk/index.php")], ["Late-license penalty not found."]),
 ("register a vehicle?", "car",
  ["Register with the town first; the Town Clerk's office collects the town permit fee and the state fee together.",
   "Renew online with E-Reg or in person.",
   "Moving to Rindge: bring your documents and the address-change form to the Town Clerk's office."],
  [("State fees (from Dec 31, 2025)", "Title $35. Passenger vehicles up to 3,000 lb $42 a year; 3,001–5,000 lb $48; 5,001–8,000 lb $66. Motorcycles $30. Vanity plates $60 a year.")],
  "Town Clerk's office, (603) 899-5181 x107.", "RSA 261; RSA 261:153 (town permit fee).", ("official",),
  [("Motor vehicles page", G + "departments/town_clerk/motor_vehicles.php"), ("E-Reg online renewal", "https://pay.eb2gov.com/Service/Index/1422?towncode=328&source=MV&towncodemasterid=321")],
  ["The town permit-fee rate table is not on the town page."]),
 ("register to vote or vote absentee?", "vote",
  ["You can vote if you are a U.S. citizen, 18 or older on election day, and live in Rindge.",
   "Register at the Town Clerk's office, at the Supervisors of the Checklist session (Wed Oct 28, 2026, the posted deadline before the Nov 3 election), or at the polls on election day.",
   "Bring proof of citizenship, age, domicile and identity.",
   "Absentee: request a form from the Town Clerk's office. Deadlines: by mail, noon the day before the election; in person, 5 pm the day before (Mon Nov 2 for the Nov 3 election)."],
  [("Where to vote", "Rindge Memorial School Gymnasium, 58 School Street, 7 am–7 pm.")],
  "Town Clerk's office, (603) 899-5181 x107; Supervisors of the Checklist.", "RSA 654:12; RSA 657.", ("official",),
  [("Voter registration", G + "departments/town_clerk/elections-draft/voter_registration.php"), ("NH Secretary of State: register to vote", "https://www.sos.nh.gov/elections/voters/register-vote")],
  ["The town elections pages say they are under construction. The 2026 town absentee form must be replaced by a 2027 version."]),
 ("appeal my property assessment (abatement)?", "tax",
  ["Pay your bill on time. An abatement request does not stop the tax from being due.",
   "File the abatement application by March 1 after the final bill (for 2026 bills: March 1, 2027).",
   "Give specific reasons, such as a factual error or a value out of line with similar properties. Include photos or comparable sales.",
   "The town must answer in writing by July 1. No answer means denial.",
   "If denied, appeal by September 1 to the NH Board of Tax and Land Appeals ($65 fee per the town page) or Superior Court."],
  [], "Assessing, (603) 899-5181 x113; the Select Board decides.", "RSA 76:16; RSA 76:16-a.", ("official",),
  [("The abatement process", G + "departments/assessing/the_abatement_process.php"), ("RSA 76:16", "https://www.gencourt.state.nh.us/rsa/html/V/76/76-16.htm")],
  ["Confirm which form year to use (the abatement page links a 2025 form)."]),
 ("apply for a tax exemption or credit?", "tax",
  ["File form PA-29 with Assessing between the December tax bill and April 15. Attach the worksheet or documents (DD-214 for veterans).",
   "Approvals are permanent; the town sends a renewal form every 5 years.",
   "Elderly (65+): $100,000 off assessed value at 65–74, $140,000 at 75–79, $200,000 at 80+. Income under $35,000 single or $49,000 married; assets under $150,000 (not counting the home).",
   "Veterans: $500 credit; surviving spouse $700; service-connected total disability $4,500 (raised by 2026 Art. 12, press-reported)."],
  [("Other", "Disabled exemption $100,000 (same limits as elderly). Blind $15,000. Solar exemption available. Current use: file form A-10 by April 15."),
   ("State relief", "Low and moderate income homeowners can apply to NH DRA between May 1 and June 30.")],
  "Assessing, (603) 899-5181 x113.", "RSA 72:27-a, 72:39-a/b, 72:28, 72:35, 72:62, 79-A.", ("official",),
  [("Exemptions and credits", G + "departments/assessing/exemptions___credits.php"), ("Assessing forms", G + "departments/assessing/forms_and_applications.php")],
  ["The 2020 report printed a $50,000 married income limit; the 2025 report says $49,000.", "Residency rules differ between the town page (1 year for veterans) and the worksheet (3 or 5 years)."]),
 ("file a citizen petition for the March ballot?", "petition",
  ["Get 25 registered Rindge voters to sign (RSA 39:3).",
   "Submit it to the Select Board by the second Tuesday in January: Jan 12, 2027 (derived from statute; confirm with the town).",
   "Zoning petitions have an earlier window: Nov 9 – Dec 9, 2026 (derived)."],
  [("Step-by-step", "See the flow diagrams in the Laws section.")],
  "Select Board office, (603) 899-5181 x101.", "RSA 39:3; RSA 40:13; RSA 675:4.", ("derived", "unconf"),
  [("How a citizen petition works", "#laws")], []),
 ("go to or watch a meeting?", "calendar",
  ["Select Board: usually every other Wednesday, 6 pm, Town Offices Conference Room. Planning Board: 1st and 3rd Tuesday, 7 pm. ZBA: 4th Tuesday, 7 pm.",
   "Meetings are open to the public. Agendas are posted on each board's page.",
   "Select Board meetings stream on Town Hall Streams."],
  [], "Select Board office, (603) 899-5181 x100.", "RSA 91-A (open meetings).", ("official",),
  [("Town Hall Streams", "https://townhallstreams.com/towns/rindge_nh"), ("Select Board agendas and minutes", O + "boards_commission/board_of_selectmen/agendas_minutes.php")],
  ["No official video links are posted for the Planning Board, ZBA or Conservation Commission."]),
 ("sign up for emergency alerts?", "bell",
  ["Rindge is moving to NH Alerts (the state system, powered by Genasys Protect).",
   "Register on the state Genasys portal for calls, texts and email, or use the free Genasys Protect app.",
   "For town news by email, sign up for eNotify."],
  [], "Fire Department / Emergency Management, (603) 899-3324.", "", ("official",),
  [("Town alert sign-up (Genasys)", "https://rindgenh.genasys.com/portal/en/register?dc=2nrz0z20pbl"), ("eNotify", G + "enotify/index.php")], []),
]

# ---- Budget and finances
BUDGET_STATS = [
 ("$5,654,177", "2026 default budget, in effect because the proposed $5,810,000 budget failed 707-824 (press)", ("official",)),
 ("$5,486,133", "2025 actual spending, against a $5,487,882 default budget", ("official",)),
 ("$856,811", "Capital reserves at end of 2025 (down from $906,320 at end of 2024)", ("official",)),
 ("$170,363", "2025 debt service: $130,000 principal plus $40,363 interest", ("official",)),
]
# dept, 2025 orig/default, 2025 actual, 2026 proposed, 2026 default (AR2025 pdf 72-83)
DEPTBUD = [
 ("Executive", 148271, 99895, 165090, 148271), ("Town Clerk", 119360, 110854, 120263, 123221), ("Election & registration", 15786, 13054, 19407, 15786),
 ("Town Office", 292260, 223992, 186937, 295460), ("Tax Collector", 74132, 72105, 76773, 74132), ("Treasurer", 5773, 5829, 5766, 5773),
 ("Technology", 113777, 113568, 77645, 113777), ("Trustee of Trust Funds", 255, 121, 255, 255), ("Assessing", 42801, 79479, 53999, 42801),
 ("Legal", 15000, 31428, 15000, 15000), ("Planning Board", 106244, 90204, 128060, 106244), ("Board of Adjustment", 10194, 7101, 17115, 10194),
 ("Town buildings", 242138, 321354, 267827, 251138), ("Cemeteries", 2081, 9110, 8100, 2081), ("Insurance", 137973, 155198, 164373, 155397),
 ("History", 4100, 4100, 4100, 4100), ("Police", 1322817, 1314820, 1362159, 1322817), ("Ambulance", 46500, 98000, 85000, 85000),
 ("Fire", 627664, 635460, 617369, 637942), ("Mutual aid", 73983, 78422, 125000, 125000), ("Emergency management", 15604, 10172, 14970, 15604),
 ("Highway", 850420, 817750, 900305, 866920), ("Highway projects", 273591, 236265, 273591, 273591), ("Highway block grant", 176492, 176492, 176492, 176492),
 ("Street lights", 6000, 3662, 5000, 6000), ("Solid waste", 166190, 178968, 206208, 201190), ("Welfare", 33698, 44346, 34355, 34355),
 ("Recreation", 118330, 122449, 122067, 118330), ("Parks & playgrounds", 6033, 1020, 3502, 6033), ("Library", 242330, 243205, 252430, 242330),
 ("Patriotic purposes", 2200, 2089, 4100, 2200), ("Conservation Commission", 6380, 4775, 6380, 6380), ("Note payable (principal)", 130000, 130000, 130000, 130000),
 ("Interest, long-term bond", 42443, 40363, 40363, 40363),
]
DEPTBUD_TOT = (5487882, 5486133, 5810000, 5654177)
# fund, end 2025, end 2024
RESERVES = [
 ("Bridge Maintenance", 139042.19, 137637.63), ("Ingalls Library", 106147.06, 85278.25), ("Fire Dept. Equipment", 104784.33, 188148.65),
 ("Highway Dept. Equipment", 101330.68, 100308.61), ("Revaluation", 82202.71, 112877.02), ("Building Maintenance", 78841.30, 99496.93),
 ("Recreation Facilities", 75766.54, 50255.15), ("Meeting House Maint.", 62261.05, 61644.70), ("Ambulance Service Expendable", 40000.00, None),
 ("Rec Bldg & Grounds & Well", 27296.11, 27025.07), ("Conservation Commission", 12859.64, 12743.73), ("Cemetery", 11110.51, 15879.52),
 ("Police Dept. Equipment", 10579.36, 10475.57), ("Rindge Comm. Center", 3680.29, 3649.98), ("Recycling Program", 810.41, 802.22), ("Library Remodeling", 98.35, 97.35),
]
RES_TOT = (856810.52, 906320.38)
# 2025 money articles (official, AR2025) and 2026 (press)
ART25 = [
 ("Art 11: unused bond proceeds for Town Office HVAC, $60,375 (needs 3/5)", 576, 1045, False), ("Art 12: ambulance service, $38,500", 1181, 457, True),
 ("Art 13: Ambulance Service Expendable Trust, $40,000", 971, 663, True), ("Art 14: Fire Dept. Equipment CRF, $145,000", 779, 840, False),
 ("Art 15: Revaluation CRF, $25,000", 872, 736, True), ("Art 16: Highway Dept. CRF, $150,000", 717, 902, False),
 ("Art 17: Municipal Building CRF, $100,000 (needs 2/3)", 501, 1130, False), ("Art 18: Police Equipment CRF, $50,000", 653, 967, False),
 ("Art 19: Ingalls Library ETF, $20,000", 861, 771, True), ("Art 20: Recreation Facilities CRF, $25,000", 913, 704, True),
 ("Art 21: Meetinghouse Maintenance ETF, $25,000", 767, 845, False), ("Art 23: tenth police officer, $93,591", 347, 1300, False),
]
ART26 = [
 ("Art 4: Highway Dept. equipment CRF, $185,000", 1004, 526, True), ("Art 5: Fire Dept. Equipment CRF, $125,000", 1082, 446, True),
 ("Art 6: Ambulance Service ETF, $40,000", 1307, 230, True), ("Art 7: Building Maintenance CRF, $35,000", 1060, 465, True),
 ("Art 8: Recreation Facilities CRF, $25,000", 1095, 438, True), ("Art 9: Meetinghouse Maintenance ETF, $25,000", 996, 535, True),
 ("Art 10: Ingalls Memorial Library ETF, $20,000", 1171, 361, True),
]
ART26_NOTFOUND = "Results for 2026 Art 11 (250th celebration, $5,000), Art 12 (veterans' disability credit), Art 13 (farm structures) and Art 14 (Land Use Change Tax) were not found in the press articles read; other sources on this page report some as passed without tallies."
DEBT = [
 ("2020 fiber-to-the-premises bond: total project $5,037,825, of which $2,579,125 was bonded and the rest contributed by Consolidated Communications. Passed 1,151-174. Bond proceeds received Aug 13, 2020.", ("official",)),
 ("Debt service in the budget: $130,000 principal and $40,363 interest in 2025; the same amounts in the 2026 default budget.", ("official",)),
 ("The $130,000 a year of principal appears to be for the 2020 fiber bond. The annual reports do not say so; this is an inference.", ("infer",)),
 ("The town receives $186,000 a year from Consolidated Communications (CCI Fiber) and held $742,847 in the CCI Fiber account at the end of 2025.", ("official",)),
 ("2025 Art 11, to spend $60,375 of unused bond proceeds on the Town Office HVAC, failed 576-1,045 (needed 3/5).", ("official",)),
]
CIP = [
 ("Fall 2025 CIP recommendations for the 2026 warrant: Fire $150,000; Highway $165,000; facilities $35,000; Recreation $50,000; Library $20,000; Meetinghouse $25,000 (total $445,000). The warrant that went to voters: Highway $185,000, Fire $125,000, Building $35,000, Recreation $25,000, Library $20,000, Meetinghouse $25,000.", ("official",)),
 ("2024 CIP recommendations for the 2025 warrant totaled $565,000. In March 2025 the Fire, Highway, Building, Police and Meetinghouse articles failed; Revaluation, Library and Recreation passed.", ("official",)),
]
FIN_NOTES = [
 ("The 2025 and 2024 tax rates ($13.79 and $25.31) are not comparable. The 2025 revaluation roughly doubled assessed values (net valuation $1,466,136,314), so the rate per $1,000 fell. It does not mean bills were cut in half.", ("official",)),
 ("2025 gross appropriations of $6,134,500 appear on the tax-rate calculation page, but the figure is from a scan and uncertain.", ("scan",)),
 ("2026 vote results are press-reported (Monadnock Ledger-Transcript, Mar 11, 2026). The town's results sheet was not located.", ("press",)),
 ("The 2023 and 2024 annual reports both print 497-256 for the operating budget. Both are withheld pending a check of the ballots.", ("withheld",)),
]
FIN_GAPS = ["A schedule of long-term debt (outstanding principal, interest rate, maturity) is not printed in any 2011–2025 annual report.",
 "The 2026 tax rate has not been set or found.", "No multi-year Capital Improvement Program table was found online; only yearly committee recommendations.",
 "The school district budget is not in the town report (see Schools and community).", "A FY2027 draft town budget was not found."]

# ---- Schools and community
SCHOOLS = [
 ("Rindge Memorial School", "PreK–5", "58 School Street, Rindge", "(603) 899-3363", "324"),
 ("Conant Middle School (grades 6–8)", "6–8", "1 Conant Way, Jaffrey", "(603) 532-8122", "241"),
 ("Conant High School (grades 9–12)", "9–12", "3 Conant Way, Jaffrey", "(603) 532-8131", "336"),
 ("Jaffrey Grade School", "PreK–5", "18 School Street, Jaffrey", "(603) 532-8355", "250"),
]
SAU = ("Jaffrey-Rindge Cooperative School District (SAU 47)", "1 Conant Way, Jaffrey, NH 03452 · (603) 532-8122", "https://sau47.org",
       "The School Board meets the 1st and 3rd Monday, public session 6:30 pm unless the agenda says otherwise. Agendas usually post the Thursday or Friday before; videos the same week.")
SCHOOL_VOTES = [
 ("March 2025: a $22.9M career and technical education (CTE) expansion was defeated; Rindge voted 1,074-611 against.", "https://ledgertranscript.com/2025/03/14/jaffrey-rindge-cte-59443211/"),
 ("March 2025: the $30.76M school budget passed after a $3M cut; Rindge voted 1,011-682 in favor.", "https://ledgertranscript.com/2025/03/18/jaffrey-rindge-budget-59443183/"),
 ("March 2026: the $33.5M school budget failed districtwide by 68 votes; Rindge voted 943-608 against.", "https://ledgertranscript.com/2026/03/11/jaffrey-rindge-school-district-voters-fail-budget/"),
]
COMMUNITY = [
 ("Library", "Ingalls Memorial Library, 203 Main Street, (603) 899-3303. Story time Mon/Wed 10:30; Lego Club; STEM third Tuesday; online author talks this fall.", ("official",), "https://www.ingallslibrary.com/"),
 ("Recreation", "Wellington Park, 283 Wellington Road, (603) 899-6847. Online registration; Rec Building (capacity 150) and pavilion rentals. The rental FAQ still mentions Covid procedures.", ("official", "stale"), G + "departments/recreation/index.php"),
 ("Lakes and ponds", "Lake Monomonac, Contoocook Lake, Emerson, Grassy, Hubbard, Bullet, Pool, Crowcroft and Pearly Ponds; Annett State Forest. Boat launch and beach details come from third-party listings (unconfirmed).", ("official",), G + "community/index.php"),
 ("Trails and conservation land", "Conservation Commission trail guide and conservation lands (Converse Meadow, School House No. 4). Fall hike Sun Oct 18, 2026, 1:30 pm, Converse Meadow.", ("official",), G + "boards_commission/conservation_commission/rindge_conservation_lands.php"),
 ("Franklin Pierce University", "40 University Drive. The Town & Gown Committee meets the 3rd Tuesday, 2 pm.", ("official",), "https://www.franklinpierce.edu/about/locations/rindge.html"),
 ("Cathedral of the Pines", "Open Mon–Fri 10–5 (May–Oct) and 9–4 (Nov–Apr); grounds dawn to dusk year-round.", ("official",), "https://www.cathedralofthepines.org/contact/"),
 ("Rindge Food Pantry", "Butternut Building, 646 NH Route 119 (lower level), (603) 899-5031.", ("official",), G + "community/clubs_and_organizations.php"),
 ("Rindge Chamber of Commerce", "P.O. Box 911, (603) 899-5051. Annual Gala every January.", ("official",), "https://www.rindgechamber.org/"),
 ("Historical Society", "24 School Street, (603) 899-2341. Museum Wed 10–12 and first Saturday 10–2, or by appointment.", ("official",), "http://rindgehistoricalsociety.org/"),
]
EVENTS = [
 ("Mon Oct 12, 2026", "Columbus Day: town offices closed (Town Clerk holiday list).", ("official",)),
 ("Sun Oct 18, 2026", "Conservation Commission fall hike, Converse Meadow, 1:30 pm.", ("official",)),
 ("Tue Oct 20, Fri Oct 23, Sat Oct 31, 2026", "Halloween events: Franklin Pierce trick-or-treat (Oct 20, 5–7 pm), Rec Department Trunk-or-Treat (Oct 23, 6–8 pm), town-wide trick-or-treat (Oct 31, 4–7 pm). Stated at the Oct 7 Select Board meeting; check the town calendar.", ("audio",)),
 ("Wed Oct 28, 2026", "Supervisors of the Checklist session, the voter registration deadline before the general election (time posted by Oct 15). New Hampshire also allows registration at the polls.", ("official",)),
 ("Tue Nov 3, 2026", "State general election, Rindge Memorial School gym, 7 am–7 pm. The ballot includes the statewide school tax-cap question (HB 1300).", ("official",)),
]

# ---- Emergency and utilities
EMERG = [
 ("Emergency", "Dial 911 for police, fire or medical emergencies.", ("official",), ""),
 ("Police, non-emergency", "(603) 899-5009, Mon–Fri 8–4. After hours (603) 355-2000. 158 Main Street.", ("official",), G + "departments/police/index.php"),
 ("Fire Department", "(603) 899-3324, 150 Main Street. The Fire Chief is also the Emergency Management Director.", ("official",), G + "departments/fire/index.php"),
 ("Ambulance", "Jaffrey-Rindge Memorial Ambulance serves Rindge through Dec 31, 2026. Peterborough Fire & Rescue takes over Jan 1, 2027 (Select Board vote 2-0-1, Sept 9, 2026, press-reported; the contract is subject to voter approval).", ("press",), "https://ledgertranscript.com/2026/09/14/rindge-ends-jrma-contract/"),
 ("Alerts", "Rindge is moving to NH Alerts (Genasys Protect). Register on the state portal or use the free app. Town news by email: eNotify.", ("official",), "https://rindgenh.genasys.com/portal/en/register?dc=2nrz0z20pbl"),
 ("Shelters and warming centers", "The 2019 emergency plan lists the Recreation Department and Rindge Memorial School as mass-care resources. No currently designated shelter or warming center is confirmed (UNCONFIRMED). The town is updating its emergency plan.", ("official", "unconf"), ""),
 ("Non-emergency help", "Dial 211 for statewide help lines.", ("official",), ""),
 ("Roads and snow", "Public Works, (603) 899-2105. The snow and ice policy is available at the Town Office.", ("official",), G + "departments/public_works/index.php"),
 ("Health Officer", "(603) 899-5181 x100.", ("official",), G + "departments/health_officer/index.php"),
]
UTIL = [
 ("Electricity", "Eversource is the utility. Residents can opt in to Community Power (Community Power Coalition of NH). The Energy Commission page cites $0.086/kWh versus Eversource's $0.10403 default, with no date; check current rates.", ("official", "stale"), G + "boards_commission/energy_commission/index.php"),
 ("Water and sewer", "No municipal water or sewer system is listed for Rindge, consistent with private wells and septic systems (UNCONFIRMED; ask the Town Office or NH DES).", ("unconf",), ""),
 ("Trash and recycling", "Transfer station, 113 Main Street: Tue 10–7, Thu 10–7, Fri 1–7, Sat 8–3. Stickers $50 ($25 for one senior per household), sold at the Town Clerk's or Selectmen's office. No town curbside pickup confirmed (UNCONFIRMED).", ("official",), G + "departments/recycling_transfer_station/index.php"),
 ("Broadband", "A town-owned fiber network built in 2020–21 with Consolidated Communications (marketed as Fidium Fiber), financed by a ~$2.6M bond repaid from capped subscriber fees, not taxes, per press reports. The town receives $186,000 a year.", ("press",), "https://ledgertranscript.com/2020/01/17/rindge-to-bond-for-better-internet-32026308/"),
]

# ---- Town facts and history
FACTS = [
 ("Incorporated", "1768 (Feb 11, 1768 per the Historical Society), named for Capt. Daniel Rindge of Portsmouth. Granted in 1736 by Massachusetts as \"Rowley-Canada\" and regranted in 1749 as \"Monadnock No. 1\".", ("official",)),
 ("Population", "6,476 (2020 Census); 6,014 (2010); 6,502 estimated for July 1, 2025. The first census, in 1790, counted 1,143. NH Employment Security shows slightly different figures; the Census count is official.", ("official",)),
 ("Area", "39.8 square miles: 37.1 land and 2.7 inland water. Elevation about 1,316 ft. ZIP 03461, area code 603, Cheshire County, on the Massachusetts border. Routes 119 and 202.", ("official",)),
 ("Villages and places", "Rindge Center, Converseville, East Rindge, West Rindge, Cutter Hill, Jones Corner, Rand, Thomas, Woodmere.", ("official",)),
 ("Government", "Select Board (3 members) and Town Administrator. SB2 official-ballot town meeting: Deliberative Session in late January or early February, vote on the second Tuesday of March (next: Tue Mar 9, 2027, derived).", ("official",)),
 ("Landmarks", "Cathedral of the Pines; Franklin Pierce University; the Rindge Meeting House; Ingalls Memorial Library; Hillside and Meetinghouse cemeteries; the Town Common and gazebo.", ("official",)),
 ("Town histories", "Stearns, History of Rindge, NH 1736–1874, and Town on the Border, Rindge 1874–1988 (box set $55 at the Town Office).", ("official",)),
 ("Historical Society museum", "The town page names both the Hoyt-Allen house (c.1800–1840) and the Freeborn Stearns house (c.1815) for the museum (UNCONFIRMED which).", ("official", "unconf")),
]
FACT_LINKS = [("NH Employment Security community profile", "https://www2.nhes.nh.gov/GraniteStats/SessionServlet?city=000314&cityName=Rindge&page=Community.jsp"),
              ("US Census QuickFacts", "https://www.census.gov/quickfacts/fact/table/rindgetowncheshirecountynewhampshire/POP645224"),
              ("Rindge Historical Society", "http://rindgehistoricalsociety.org/")]
