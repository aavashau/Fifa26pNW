"""
FIFA World Cup 2026 — Official fixture schedule.
All times stored in UTC. Source: Wikipedia / FIFA official schedule.
Nepal Standard Time (NPT) = UTC + 5:45
"""

# Each match: match_code, stage, home_team, away_team, venue, match_time_utc (ISO UTC), notes

GROUP_STAGE: list[dict] = [
    # ── GROUP A: Mexico · South Korea · Czech Republic · South Africa ──
    {"match_code": "A1",  "stage": "Group A", "home_team": "Mexico",       "away_team": "South Africa", "venue": "Estadio Azteca, Mexico City",          "match_time_utc": "2026-06-11T19:00:00+00:00", "notes": "MD1"},
    {"match_code": "A2",  "stage": "Group A", "home_team": "South Korea",  "away_team": "Czech Republic","venue": "Estadio Akron, Zapopan",               "match_time_utc": "2026-06-12T02:00:00+00:00", "notes": "MD1"},
    {"match_code": "A3",  "stage": "Group A", "home_team": "Czech Republic","away_team": "South Africa", "venue": "Mercedes-Benz Stadium, Atlanta",       "match_time_utc": "2026-06-18T16:00:00+00:00", "notes": "MD2"},
    {"match_code": "A4",  "stage": "Group A", "home_team": "Mexico",       "away_team": "South Korea",  "venue": "Estadio Akron, Zapopan",               "match_time_utc": "2026-06-19T01:00:00+00:00", "notes": "MD2"},
    {"match_code": "A5",  "stage": "Group A", "home_team": "Czech Republic","away_team": "Mexico",       "venue": "Estadio Azteca, Mexico City",          "match_time_utc": "2026-06-25T01:00:00+00:00", "notes": "MD3"},
    {"match_code": "A6",  "stage": "Group A", "home_team": "South Africa", "away_team": "South Korea",  "venue": "Estadio BBVA, Guadalupe",              "match_time_utc": "2026-06-25T01:00:00+00:00", "notes": "MD3"},

    # ── GROUP B: Canada · Bosnia & Herzegovina · Qatar · Switzerland ──
    {"match_code": "B1",  "stage": "Group B", "home_team": "Canada",               "away_team": "Bosnia and Herzegovina", "venue": "BMO Field, Toronto",          "match_time_utc": "2026-06-12T19:00:00+00:00", "notes": "MD1"},
    {"match_code": "B2",  "stage": "Group B", "home_team": "Qatar",                "away_team": "Switzerland",            "venue": "Levi's Stadium, Santa Clara",  "match_time_utc": "2026-06-13T19:00:00+00:00", "notes": "MD1"},
    {"match_code": "B3",  "stage": "Group B", "home_team": "Switzerland",          "away_team": "Bosnia and Herzegovina", "venue": "SoFi Stadium, Inglewood",     "match_time_utc": "2026-06-18T19:00:00+00:00", "notes": "MD2"},
    {"match_code": "B4",  "stage": "Group B", "home_team": "Canada",               "away_team": "Qatar",                  "venue": "BC Place, Vancouver",          "match_time_utc": "2026-06-18T22:00:00+00:00", "notes": "MD2"},
    {"match_code": "B5",  "stage": "Group B", "home_team": "Switzerland",          "away_team": "Canada",                 "venue": "BC Place, Vancouver",          "match_time_utc": "2026-06-24T19:00:00+00:00", "notes": "MD3"},
    {"match_code": "B6",  "stage": "Group B", "home_team": "Bosnia and Herzegovina","away_team": "Qatar",                 "venue": "Lumen Field, Seattle",         "match_time_utc": "2026-06-24T19:00:00+00:00", "notes": "MD3"},

    # ── GROUP C: Brazil · Morocco · Haiti · Scotland ──
    {"match_code": "C1",  "stage": "Group C", "home_team": "Brazil",   "away_team": "Morocco",  "venue": "MetLife Stadium, East Rutherford",     "match_time_utc": "2026-06-13T22:00:00+00:00", "notes": "MD1"},
    {"match_code": "C2",  "stage": "Group C", "home_team": "Haiti",    "away_team": "Scotland", "venue": "Gillette Stadium, Foxborough",         "match_time_utc": "2026-06-14T01:00:00+00:00", "notes": "MD1"},
    {"match_code": "C3",  "stage": "Group C", "home_team": "Scotland", "away_team": "Morocco",  "venue": "Gillette Stadium, Foxborough",         "match_time_utc": "2026-06-19T22:00:00+00:00", "notes": "MD2"},
    {"match_code": "C4",  "stage": "Group C", "home_team": "Brazil",   "away_team": "Haiti",    "venue": "Lincoln Financial Field, Philadelphia","match_time_utc": "2026-06-20T00:30:00+00:00", "notes": "MD2"},
    {"match_code": "C5",  "stage": "Group C", "home_team": "Scotland", "away_team": "Brazil",   "venue": "Hard Rock Stadium, Miami Gardens",     "match_time_utc": "2026-06-24T22:00:00+00:00", "notes": "MD3"},
    {"match_code": "C6",  "stage": "Group C", "home_team": "Morocco",  "away_team": "Haiti",    "venue": "Mercedes-Benz Stadium, Atlanta",       "match_time_utc": "2026-06-24T22:00:00+00:00", "notes": "MD3"},

    # ── GROUP D: United States · Paraguay · Australia · Turkey ──
    {"match_code": "D1",  "stage": "Group D", "home_team": "United States", "away_team": "Paraguay",   "venue": "SoFi Stadium, Inglewood",      "match_time_utc": "2026-06-13T01:00:00+00:00", "notes": "MD1"},
    {"match_code": "D2",  "stage": "Group D", "home_team": "Australia",     "away_team": "Turkey",     "venue": "BC Place, Vancouver",           "match_time_utc": "2026-06-14T04:00:00+00:00", "notes": "MD1"},
    {"match_code": "D3",  "stage": "Group D", "home_team": "United States", "away_team": "Australia",  "venue": "Lumen Field, Seattle",          "match_time_utc": "2026-06-19T19:00:00+00:00", "notes": "MD2"},
    {"match_code": "D4",  "stage": "Group D", "home_team": "Turkey",        "away_team": "Paraguay",   "venue": "Levi's Stadium, Santa Clara",   "match_time_utc": "2026-06-20T03:00:00+00:00", "notes": "MD2"},
    {"match_code": "D5",  "stage": "Group D", "home_team": "Turkey",        "away_team": "United States","venue": "SoFi Stadium, Inglewood",     "match_time_utc": "2026-06-26T02:00:00+00:00", "notes": "MD3"},
    {"match_code": "D6",  "stage": "Group D", "home_team": "Paraguay",      "away_team": "Australia",  "venue": "Levi's Stadium, Santa Clara",   "match_time_utc": "2026-06-26T02:00:00+00:00", "notes": "MD3"},

    # ── GROUP E: Germany · Curaçao · Ivory Coast · Ecuador ──
    {"match_code": "E1",  "stage": "Group E", "home_team": "Germany",     "away_team": "Curaçao",     "venue": "NRG Stadium, Houston",                 "match_time_utc": "2026-06-14T17:00:00+00:00", "notes": "MD1"},
    {"match_code": "E2",  "stage": "Group E", "home_team": "Ivory Coast", "away_team": "Ecuador",     "venue": "Lincoln Financial Field, Philadelphia", "match_time_utc": "2026-06-14T23:00:00+00:00", "notes": "MD1"},
    {"match_code": "E3",  "stage": "Group E", "home_team": "Germany",     "away_team": "Ivory Coast", "venue": "BMO Field, Toronto",                   "match_time_utc": "2026-06-20T20:00:00+00:00", "notes": "MD2"},
    {"match_code": "E4",  "stage": "Group E", "home_team": "Ecuador",     "away_team": "Curaçao",     "venue": "Arrowhead Stadium, Kansas City",        "match_time_utc": "2026-06-21T00:00:00+00:00", "notes": "MD2"},
    {"match_code": "E5",  "stage": "Group E", "home_team": "Curaçao",     "away_team": "Ivory Coast", "venue": "Lincoln Financial Field, Philadelphia", "match_time_utc": "2026-06-25T20:00:00+00:00", "notes": "MD3"},
    {"match_code": "E6",  "stage": "Group E", "home_team": "Ecuador",     "away_team": "Germany",     "venue": "MetLife Stadium, East Rutherford",      "match_time_utc": "2026-06-25T20:00:00+00:00", "notes": "MD3"},

    # ── GROUP F: Netherlands · Japan · Sweden · Tunisia ──
    {"match_code": "F1",  "stage": "Group F", "home_team": "Netherlands", "away_team": "Japan",       "venue": "AT&T Stadium, Arlington",       "match_time_utc": "2026-06-14T20:00:00+00:00", "notes": "MD1"},
    {"match_code": "F2",  "stage": "Group F", "home_team": "Sweden",      "away_team": "Tunisia",     "venue": "Estadio BBVA, Guadalupe",        "match_time_utc": "2026-06-15T02:00:00+00:00", "notes": "MD1"},
    {"match_code": "F3",  "stage": "Group F", "home_team": "Netherlands", "away_team": "Sweden",      "venue": "NRG Stadium, Houston",           "match_time_utc": "2026-06-20T17:00:00+00:00", "notes": "MD2"},
    {"match_code": "F4",  "stage": "Group F", "home_team": "Tunisia",     "away_team": "Japan",       "venue": "Estadio BBVA, Guadalupe",        "match_time_utc": "2026-06-21T04:00:00+00:00", "notes": "MD2"},
    {"match_code": "F5",  "stage": "Group F", "home_team": "Japan",       "away_team": "Sweden",      "venue": "AT&T Stadium, Arlington",       "match_time_utc": "2026-06-25T23:00:00+00:00", "notes": "MD3"},
    {"match_code": "F6",  "stage": "Group F", "home_team": "Tunisia",     "away_team": "Netherlands", "venue": "Arrowhead Stadium, Kansas City", "match_time_utc": "2026-06-25T23:00:00+00:00", "notes": "MD3"},

    # ── GROUP G: Belgium · Egypt · Iran · New Zealand ──
    {"match_code": "G1",  "stage": "Group G", "home_team": "Belgium",     "away_team": "Egypt",       "venue": "Lumen Field, Seattle",    "match_time_utc": "2026-06-15T19:00:00+00:00", "notes": "MD1"},
    {"match_code": "G2",  "stage": "Group G", "home_team": "Iran",        "away_team": "New Zealand", "venue": "SoFi Stadium, Inglewood", "match_time_utc": "2026-06-16T01:00:00+00:00", "notes": "MD1"},
    {"match_code": "G3",  "stage": "Group G", "home_team": "Belgium",     "away_team": "Iran",        "venue": "SoFi Stadium, Inglewood", "match_time_utc": "2026-06-21T19:00:00+00:00", "notes": "MD2"},
    {"match_code": "G4",  "stage": "Group G", "home_team": "New Zealand", "away_team": "Egypt",       "venue": "BC Place, Vancouver",     "match_time_utc": "2026-06-22T01:00:00+00:00", "notes": "MD2"},
    {"match_code": "G5",  "stage": "Group G", "home_team": "Egypt",       "away_team": "Iran",        "venue": "Lumen Field, Seattle",    "match_time_utc": "2026-06-27T03:00:00+00:00", "notes": "MD3"},
    {"match_code": "G6",  "stage": "Group G", "home_team": "New Zealand", "away_team": "Belgium",     "venue": "BC Place, Vancouver",     "match_time_utc": "2026-06-27T03:00:00+00:00", "notes": "MD3"},

    # ── GROUP H: Spain · Cape Verde · Saudi Arabia · Uruguay ──
    {"match_code": "H1",  "stage": "Group H", "home_team": "Spain",        "away_team": "Cape Verde",   "venue": "Mercedes-Benz Stadium, Atlanta",   "match_time_utc": "2026-06-15T16:00:00+00:00", "notes": "MD1"},
    {"match_code": "H2",  "stage": "Group H", "home_team": "Saudi Arabia", "away_team": "Uruguay",      "venue": "Hard Rock Stadium, Miami Gardens", "match_time_utc": "2026-06-15T22:00:00+00:00", "notes": "MD1"},
    {"match_code": "H3",  "stage": "Group H", "home_team": "Spain",        "away_team": "Saudi Arabia", "venue": "Mercedes-Benz Stadium, Atlanta",   "match_time_utc": "2026-06-21T16:00:00+00:00", "notes": "MD2"},
    {"match_code": "H4",  "stage": "Group H", "home_team": "Uruguay",      "away_team": "Cape Verde",   "venue": "Hard Rock Stadium, Miami Gardens", "match_time_utc": "2026-06-21T22:00:00+00:00", "notes": "MD2"},
    {"match_code": "H5",  "stage": "Group H", "home_team": "Cape Verde",   "away_team": "Saudi Arabia", "venue": "NRG Stadium, Houston",             "match_time_utc": "2026-06-27T00:00:00+00:00", "notes": "MD3"},
    {"match_code": "H6",  "stage": "Group H", "home_team": "Uruguay",      "away_team": "Spain",        "venue": "Estadio Akron, Zapopan",           "match_time_utc": "2026-06-27T00:00:00+00:00", "notes": "MD3"},

    # ── GROUP I: France · Senegal · Iraq · Norway ──
    {"match_code": "I1",  "stage": "Group I", "home_team": "France",  "away_team": "Senegal", "venue": "MetLife Stadium, East Rutherford",      "match_time_utc": "2026-06-16T19:00:00+00:00", "notes": "MD1"},
    {"match_code": "I2",  "stage": "Group I", "home_team": "Iraq",    "away_team": "Norway",  "venue": "Gillette Stadium, Foxborough",          "match_time_utc": "2026-06-16T22:00:00+00:00", "notes": "MD1"},
    {"match_code": "I3",  "stage": "Group I", "home_team": "France",  "away_team": "Iraq",    "venue": "Lincoln Financial Field, Philadelphia", "match_time_utc": "2026-06-22T21:00:00+00:00", "notes": "MD2"},
    {"match_code": "I4",  "stage": "Group I", "home_team": "Norway",  "away_team": "Senegal", "venue": "MetLife Stadium, East Rutherford",      "match_time_utc": "2026-06-23T00:00:00+00:00", "notes": "MD2"},
    {"match_code": "I5",  "stage": "Group I", "home_team": "Norway",  "away_team": "France",  "venue": "Gillette Stadium, Foxborough",          "match_time_utc": "2026-06-26T19:00:00+00:00", "notes": "MD3"},
    {"match_code": "I6",  "stage": "Group I", "home_team": "Senegal", "away_team": "Iraq",    "venue": "BMO Field, Toronto",                    "match_time_utc": "2026-06-26T19:00:00+00:00", "notes": "MD3"},

    # ── GROUP J: Argentina · Algeria · Austria · Jordan ──
    {"match_code": "J1",  "stage": "Group J", "home_team": "Argentina", "away_team": "Algeria", "venue": "Arrowhead Stadium, Kansas City", "match_time_utc": "2026-06-17T01:00:00+00:00", "notes": "MD1"},
    {"match_code": "J2",  "stage": "Group J", "home_team": "Austria",   "away_team": "Jordan",  "venue": "Levi's Stadium, Santa Clara",   "match_time_utc": "2026-06-17T04:00:00+00:00", "notes": "MD1"},
    {"match_code": "J3",  "stage": "Group J", "home_team": "Argentina", "away_team": "Austria", "venue": "AT&T Stadium, Arlington",       "match_time_utc": "2026-06-22T17:00:00+00:00", "notes": "MD2"},
    {"match_code": "J4",  "stage": "Group J", "home_team": "Jordan",    "away_team": "Algeria", "venue": "Levi's Stadium, Santa Clara",   "match_time_utc": "2026-06-23T03:00:00+00:00", "notes": "MD2"},
    {"match_code": "J5",  "stage": "Group J", "home_team": "Algeria",   "away_team": "Austria", "venue": "Arrowhead Stadium, Kansas City", "match_time_utc": "2026-06-28T02:00:00+00:00", "notes": "MD3"},
    {"match_code": "J6",  "stage": "Group J", "home_team": "Jordan",    "away_team": "Argentina","venue": "AT&T Stadium, Arlington",      "match_time_utc": "2026-06-28T02:00:00+00:00", "notes": "MD3"},

    # ── GROUP K: Portugal · DR Congo · Uzbekistan · Colombia ──
    {"match_code": "K1",  "stage": "Group K", "home_team": "Portugal",    "away_team": "DR Congo",   "venue": "NRG Stadium, Houston",             "match_time_utc": "2026-06-17T17:00:00+00:00", "notes": "MD1"},
    {"match_code": "K2",  "stage": "Group K", "home_team": "Uzbekistan",  "away_team": "Colombia",   "venue": "Estadio Azteca, Mexico City",       "match_time_utc": "2026-06-18T02:00:00+00:00", "notes": "MD1"},
    {"match_code": "K3",  "stage": "Group K", "home_team": "Portugal",    "away_team": "Uzbekistan", "venue": "NRG Stadium, Houston",             "match_time_utc": "2026-06-23T17:00:00+00:00", "notes": "MD2"},
    {"match_code": "K4",  "stage": "Group K", "home_team": "Colombia",    "away_team": "DR Congo",   "venue": "Estadio Akron, Zapopan",           "match_time_utc": "2026-06-24T02:00:00+00:00", "notes": "MD2"},
    {"match_code": "K5",  "stage": "Group K", "home_team": "Colombia",    "away_team": "Portugal",   "venue": "Hard Rock Stadium, Miami Gardens", "match_time_utc": "2026-06-27T23:30:00+00:00", "notes": "MD3"},
    {"match_code": "K6",  "stage": "Group K", "home_team": "DR Congo",    "away_team": "Uzbekistan", "venue": "Mercedes-Benz Stadium, Atlanta",   "match_time_utc": "2026-06-27T23:30:00+00:00", "notes": "MD3"},

    # ── GROUP L: England · Croatia · Ghana · Panama ──
    {"match_code": "L1",  "stage": "Group L", "home_team": "England", "away_team": "Croatia", "venue": "AT&T Stadium, Arlington",               "match_time_utc": "2026-06-17T20:00:00+00:00", "notes": "MD1"},
    {"match_code": "L2",  "stage": "Group L", "home_team": "Ghana",   "away_team": "Panama",  "venue": "BMO Field, Toronto",                    "match_time_utc": "2026-06-17T23:00:00+00:00", "notes": "MD1"},
    {"match_code": "L3",  "stage": "Group L", "home_team": "England", "away_team": "Ghana",   "venue": "Gillette Stadium, Foxborough",          "match_time_utc": "2026-06-23T20:00:00+00:00", "notes": "MD2"},
    {"match_code": "L4",  "stage": "Group L", "home_team": "Panama",  "away_team": "Croatia", "venue": "BMO Field, Toronto",                    "match_time_utc": "2026-06-23T23:00:00+00:00", "notes": "MD2"},
    {"match_code": "L5",  "stage": "Group L", "home_team": "Panama",  "away_team": "England", "venue": "MetLife Stadium, East Rutherford",      "match_time_utc": "2026-06-27T21:00:00+00:00", "notes": "MD3"},
    {"match_code": "L6",  "stage": "Group L", "home_team": "Croatia", "away_team": "Ghana",   "venue": "Lincoln Financial Field, Philadelphia", "match_time_utc": "2026-06-27T21:00:00+00:00", "notes": "MD3"},
]

KNOCKOUT_FIXTURES: list[dict] = [
    # ── ROUND OF 32 ──
    {"match_code": "R32-1",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "SoFi Stadium, Inglewood",             "match_time_utc": "2026-06-28T19:00:00+00:00", "notes": "Runner-up A vs Runner-up B"},
    {"match_code": "R32-2",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "NRG Stadium, Houston",                "match_time_utc": "2026-06-29T17:00:00+00:00", "notes": "Winner C vs Runner-up F"},
    {"match_code": "R32-3",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Gillette Stadium, Foxborough",        "match_time_utc": "2026-06-29T20:30:00+00:00", "notes": "Winner E vs Best 3rd (A/B/C/D/F)"},
    {"match_code": "R32-4",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Estadio BBVA, Guadalupe",             "match_time_utc": "2026-06-30T01:00:00+00:00", "notes": "Winner F vs Runner-up C"},
    {"match_code": "R32-5",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "AT&T Stadium, Arlington",             "match_time_utc": "2026-06-30T17:00:00+00:00", "notes": "Runner-up E vs Runner-up I"},
    {"match_code": "R32-6",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "MetLife Stadium, East Rutherford",    "match_time_utc": "2026-06-30T21:00:00+00:00", "notes": "Winner I vs Best 3rd (C/D/F/G/H)"},
    {"match_code": "R32-7",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Estadio Azteca, Mexico City",         "match_time_utc": "2026-07-01T01:00:00+00:00", "notes": "Winner A vs Best 3rd (C/E/F/H/I)"},
    {"match_code": "R32-8",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Mercedes-Benz Stadium, Atlanta",      "match_time_utc": "2026-07-01T16:00:00+00:00", "notes": "Winner L vs Best 3rd (E/H/I/J/K)"},
    {"match_code": "R32-9",  "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Lumen Field, Seattle",                "match_time_utc": "2026-07-01T20:00:00+00:00", "notes": "Winner G vs Best 3rd (A/E/H/I/J)"},
    {"match_code": "R32-10", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Levi's Stadium, Santa Clara",         "match_time_utc": "2026-07-02T00:00:00+00:00", "notes": "Winner D vs Best 3rd (B/E/F/I/J)"},
    {"match_code": "R32-11", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "SoFi Stadium, Inglewood",             "match_time_utc": "2026-07-02T19:00:00+00:00", "notes": "Winner H vs Runner-up J"},
    {"match_code": "R32-12", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "BMO Field, Toronto",                  "match_time_utc": "2026-07-02T23:00:00+00:00", "notes": "Runner-up K vs Runner-up L"},
    {"match_code": "R32-13", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "BC Place, Vancouver",                 "match_time_utc": "2026-07-03T03:00:00+00:00", "notes": "Winner B vs Best 3rd (E/F/G/I/J)"},
    {"match_code": "R32-14", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "AT&T Stadium, Arlington",             "match_time_utc": "2026-07-03T18:00:00+00:00", "notes": "Runner-up D vs Runner-up G"},
    {"match_code": "R32-15", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Hard Rock Stadium, Miami Gardens",    "match_time_utc": "2026-07-03T22:00:00+00:00", "notes": "Winner J vs Runner-up H"},
    {"match_code": "R32-16", "stage": "Round of 32", "home_team": "TBD", "away_team": "TBD", "venue": "Arrowhead Stadium, Kansas City",      "match_time_utc": "2026-07-04T01:30:00+00:00", "notes": "Winner K vs Best 3rd (D/E/I/J/L)"},

    # ── ROUND OF 16 ──
    {"match_code": "R16-1", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "NRG Stadium, Houston",                "match_time_utc": "2026-07-04T17:00:00+00:00", "notes": "W R32-1 vs W R32-3"},
    {"match_code": "R16-2", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "Lincoln Financial Field, Philadelphia","match_time_utc": "2026-07-04T21:00:00+00:00", "notes": "W R32-2 vs W R32-5"},
    {"match_code": "R16-3", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "MetLife Stadium, East Rutherford",    "match_time_utc": "2026-07-05T20:00:00+00:00", "notes": "W R32-4 vs W R32-6"},
    {"match_code": "R16-4", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "Estadio Azteca, Mexico City",         "match_time_utc": "2026-07-06T00:00:00+00:00", "notes": "W R32-7 vs W R32-8"},
    {"match_code": "R16-5", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "AT&T Stadium, Arlington",             "match_time_utc": "2026-07-06T19:00:00+00:00", "notes": "W R32-11 vs W R32-12"},
    {"match_code": "R16-6", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "Lumen Field, Seattle",                "match_time_utc": "2026-07-07T00:00:00+00:00", "notes": "W R32-9 vs W R32-10"},
    {"match_code": "R16-7", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "Mercedes-Benz Stadium, Atlanta",      "match_time_utc": "2026-07-07T16:00:00+00:00", "notes": "W R32-14 vs W R32-16"},
    {"match_code": "R16-8", "stage": "Round of 16", "home_team": "TBD", "away_team": "TBD", "venue": "BC Place, Vancouver",                 "match_time_utc": "2026-07-07T20:00:00+00:00", "notes": "W R32-13 vs W R32-15"},

    # ── QUARTER-FINALS ──
    {"match_code": "QF-1", "stage": "Quarter-Final", "home_team": "TBD", "away_team": "TBD", "venue": "Gillette Stadium, Foxborough",     "match_time_utc": "2026-07-09T20:00:00+00:00", "notes": "W R16-1 vs W R16-2"},
    {"match_code": "QF-2", "stage": "Quarter-Final", "home_team": "TBD", "away_team": "TBD", "venue": "SoFi Stadium, Inglewood",          "match_time_utc": "2026-07-10T19:00:00+00:00", "notes": "W R16-5 vs W R16-6"},
    {"match_code": "QF-3", "stage": "Quarter-Final", "home_team": "TBD", "away_team": "TBD", "venue": "Hard Rock Stadium, Miami Gardens", "match_time_utc": "2026-07-11T21:00:00+00:00", "notes": "W R16-3 vs W R16-4"},
    {"match_code": "QF-4", "stage": "Quarter-Final", "home_team": "TBD", "away_team": "TBD", "venue": "Arrowhead Stadium, Kansas City",   "match_time_utc": "2026-07-12T01:00:00+00:00", "notes": "W R16-7 vs W R16-8"},

    # ── SEMI-FINALS ──
    {"match_code": "SF-1", "stage": "Semi-Final", "home_team": "TBD", "away_team": "TBD", "venue": "AT&T Stadium, Arlington",          "match_time_utc": "2026-07-14T19:00:00+00:00", "notes": "W QF-1 vs W QF-2"},
    {"match_code": "SF-2", "stage": "Semi-Final", "home_team": "TBD", "away_team": "TBD", "venue": "Mercedes-Benz Stadium, Atlanta",   "match_time_utc": "2026-07-15T19:00:00+00:00", "notes": "W QF-3 vs W QF-4"},

    # ── THIRD PLACE ──
    {"match_code": "3RD",   "stage": "Third Place", "home_team": "TBD", "away_team": "TBD", "venue": "Hard Rock Stadium, Miami Gardens", "match_time_utc": "2026-07-18T21:00:00+00:00", "notes": "L SF-1 vs L SF-2"},

    # ── FINAL ──
    {"match_code": "FINAL", "stage": "Final",       "home_team": "TBD", "away_team": "TBD", "venue": "MetLife Stadium, East Rutherford", "match_time_utc": "2026-07-19T19:00:00+00:00", "notes": "W SF-1 vs W SF-2"},
]


def get_all_fixtures() -> list[dict]:
    return GROUP_STAGE + KNOCKOUT_FIXTURES
