# Threat Intelligence System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FAKE JOB DETECTOR SYSTEM                         │
│                  with Threat Intelligence                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
├─────────────────────────────────────────────────────────────────────┤
│  [Analyze Job] [Fake Companies] [Analytics] [Threat Intel] [Admin] │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FLASK APPLICATION                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │  Job Analysis    │  │ Threat Detection │  │  API Endpoints  │ │
│  │   Engine         │  │     Engine       │  │                 │ │
│  ├──────────────────┤  ├──────────────────┤  ├─────────────────┤ │
│  │ • Risk Scoring   │  │ • Extract Email  │  │ • /threat-intel │ │
│  │ • ML Prediction  │  │ • Extract Domain │  │ • /api/threat-  │ │
│  │ • Red Flags      │  │ • Extract Keywords│  │   feed          │ │
│  │ • Domain Check   │  │ • Store Threats  │  │                 │ │
│  └────────┬─────────┘  └────────┬─────────┘  └─────────────────┘ │
│           │                     │                                  │
└───────────┼─────────────────────┼──────────────────────────────────┘
            │                     │
            ▼                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER (SQLite)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │  ScanHistory    │  │ ThreatIndicator  │  │  FakeCompany    │  │
│  ├─────────────────┤  ├──────────────────┤  ├─────────────────┤  │
│  │ • company_name  │  │ • indicator_type │  │ • name          │  │
│  │ • risk_score    │  │ • indicator_value│  │ • scam_type     │  │
│  │ • risk_category │  │ • threat_level   │  │ • complaints    │  │
│  │ • ml_prediction │  │ • hit_count      │  │ • description   │  │
│  │ • red_flags     │  │ • first_seen     │  │                 │  │
│  │ • timestamp     │  │ • last_seen      │  │                 │  │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Threat Detection Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                    THREAT DETECTION PIPELINE                         │
└──────────────────────────────────────────────────────────────────────┘

Step 1: Job Submission
┌─────────────────────┐
│  User Submits Job   │
│  • Description      │
│  • Company Name     │
│  • HR Email         │
│  • Job Link         │
└──────────┬──────────┘
           │
           ▼
Step 2: Risk Analysis
┌─────────────────────┐
│  Analyze Job Post   │
│  • Check Keywords   │
│  • ML Prediction    │
│  • Domain Age       │
│  • HTTPS Check      │
│  • Email Mismatch   │
└──────────┬──────────┘
           │
           ▼
Step 3: Risk Scoring
┌─────────────────────┐
│  Calculate Score    │
│  Risk: 0-100        │
│  Category:          │
│  • Low (<35)        │
│  • Medium (35-65)   │
│  • High (>65)       │
└──────────┬──────────┘
           │
           ▼
Step 4: Threat Extraction (if High/Medium Risk)
┌─────────────────────┐
│  Extract Indicators │
│                     │
│  Email Threats:     │
│  ├─ Personal emails │
│  └─ Domain mismatch │
│                     │
│  Domain Threats:    │
│  ├─ Suspicious URL  │
│  └─ New domain      │
│                     │
│  Keyword Threats:   │
│  └─ Red flag combos │
└──────────┬──────────┘
           │
           ▼
Step 5: Database Storage
┌─────────────────────┐
│  Store/Update       │
│                     │
│  If Exists:         │
│  ├─ Increment hits  │
│  ├─ Update last_seen│
│  └─ Escalate level  │
│                     │
│  If New:            │
│  └─ Create record   │
└──────────┬──────────┘
           │
           ▼
Step 6: Dashboard Update
┌─────────────────────┐
│  Real-Time Update   │
│  • Metrics refresh  │
│  • Chart updates    │
│  • Table refreshes  │
│  • API data ready   │
└─────────────────────┘
```

## Threat Intelligence Dashboard

```
┌──────────────────────────────────────────────────────────────────────┐
│              THREAT INTELLIGENCE DASHBOARD                           │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         METRICS ROW                                 │
├────────────────┬────────────────┬────────────────┬─────────────────┤
│   Weekly       │    Active      │    Recent      │    Critical     │
│  High-Risk     │  Scam Types    │   Threats      │   Indicators    │
│   Threats      │                │                │                 │
│                │                │                │                 │
│     [45]       │     [12]       │     [10]       │      [5]        │
│                │                │                │                 │
└────────────────┴────────────────┴────────────────┴─────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      30-DAY TREND CHART                             │
│  Threats                                                            │
│    ^                                                                │
│ 20 │                                    ╱╲                          │
│    │                          ╱╲       ╱  ╲                         │
│ 15 │                    ╱╲   ╱  ╲    ╱    ╲                        │
│    │              ╱╲   ╱  ╲ ╱    ╲  ╱      ╲                       │
│ 10 │        ╱╲   ╱  ╲ ╱    ╲      ╲╱        ╲                      │
│    │   ╱╲  ╱  ╲ ╱    ╲                       ╲                     │
│  5 │  ╱  ╲╱    ╲                              ╲                    │
│    │ ╱                                         ╲                   │
│  0 └────────────────────────────────────────────────────────────▶  │
│      1    5    10   15   20   25   30  (Days)                      │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┬──────────────────────────────────┐
│   RECENT HIGH-RISK DETECTIONS    │    TRENDING SCAM TYPES           │
├──────────────────────────────────┼──────────────────────────────────┤
│ • QuickCash Ltd (Score: 85)      │ Advance Fee Fraud                │
│   2024-01-15 10:30               │ ████████████████░░░░ 45 cases    │
│   urgent, registration fee...    │                                  │
│                                  │ Data Entry Scam                  │
│ • HomeJobs India (Score: 78)     │ ████████████░░░░░░░░ 32 cases    │
│   2024-01-15 09:15               │                                  │
│   whatsapp, deposit...           │ Work From Home Fraud             │
│                                  │ ██████████░░░░░░░░░░ 28 cases    │
│ • DataEntry Pro (Score: 72)      │                                  │
│   2024-01-14 18:45               │ Investment Scam                  │
│   guaranteed income...           │ ████████░░░░░░░░░░░░ 21 cases    │
└──────────────────────────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│              CRITICAL THREAT INDICATORS TABLE                       │
├──────────┬─────────────────────────┬──────────┬──────┬─────────────┤
│   Type   │      Indicator          │  Level   │ Hits │  Last Seen  │
├──────────┼─────────────────────────┼──────────┼──────┼─────────────┤
│  email   │ hr.quickjobs@gmail.com  │ Critical │  67  │ 2024-01-15  │
│  domain  │ quickcash-jobs.xyz      │ Critical │  89  │ 2024-01-15  │
│  keyword │ urgent, registration... │ Critical │  53  │ 2024-01-14  │
│  email   │ recruitment@yahoo.com   │   High   │  45  │ 2024-01-14  │
│  domain  │ homejobs-india.com      │   High   │  41  │ 2024-01-13  │
└──────────┴─────────────────────────┴──────────┴──────┴─────────────┘
```

## API Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         API ENDPOINTS                                │
└──────────────────────────────────────────────────────────────────────┘

GET /api/threat-feed
│
├─ Returns: JSON Array
│
├─ Format:
│  [
│    {
│      "type": "email",
│      "value": "scam@gmail.com",
│      "level": "Critical",
│      "hits": 67,
│      "last_seen": "2024-01-15 10:30"
│    },
│    ...
│  ]
│
├─ Limit: 50 latest indicators
│
└─ Use Cases:
   ├─ External monitoring tools
   ├─ Automated blocking systems
   ├─ Alert notifications
   └─ Threat intelligence sharing

┌──────────────────────────────────────────────────────────────────────┐
│                    INTEGRATION EXAMPLE                               │
└──────────────────────────────────────────────────────────────────────┘

External System
      │
      │ HTTP GET
      ▼
┌─────────────────┐
│  /api/threat-   │
│      feed       │
└────────┬────────┘
         │
         │ JSON Response
         ▼
┌─────────────────┐
│  Process Data   │
│  • Parse JSON   │
│  • Filter Level │
│  • Take Action  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Actions        │
│  • Block Email  │
│  • Alert Admin  │
│  • Update Rules │
│  • Log Event    │
└─────────────────┘
```

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                    COMPLETE DATA FLOW                                │
└──────────────────────────────────────────────────────────────────────┘

User Input                    Processing                    Output
──────────                    ──────────                    ──────

[Job Post]                                              [Dashboard]
    │                                                        ▲
    │                                                        │
    ▼                                                        │
[Analyze]──────────▶[Risk Score]──────────▶[Store Scan]────┤
    │                    │                      │           │
    │                    │                      │           │
    │                    ▼                      │           │
    │              [High Risk?]                 │           │
    │                    │                      │           │
    │                    │ Yes                  │           │
    │                    ▼                      │           │
    │            [Extract Threats]              │           │
    │                    │                      │           │
    │                    ├─[Email]──────────────┤           │
    │                    ├─[Domain]─────────────┤           │
    │                    └─[Keywords]───────────┤           │
    │                                            │           │
    │                                            ▼           │
    │                                    [ThreatIndicator]───┤
    │                                            │           │
    │                                            │           │
    └────────────────────────────────────────────┴───────────┘
                                                             │
                                                             ▼
                                                        [API Feed]
```

## Technology Stack

```
┌──────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY LAYERS                               │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  FRONTEND                                                           │
│  • HTML5, CSS3, Bootstrap 5                                         │
│  • JavaScript, Chart.js                                             │
│  • Responsive Design                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BACKEND                                                            │
│  • Flask (Python Web Framework)                                     │
│  • SQLAlchemy (ORM)                                                 │
│  • RESTful API                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  MACHINE LEARNING                                                   │
│  • scikit-learn                                                     │
│  • TF-IDF Vectorizer                                                │
│  • Logistic Regression                                              │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  DATABASE                                                           │
│  • SQLite                                                           │
│  • Relational Schema                                                │
│  • ACID Compliance                                                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  EXTERNAL SERVICES                                                  │
│  • WHOIS (Domain Age)                                               │
│  • SSL/HTTPS Verification                                           │
│  • Chart.js CDN                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

**Legend:**
- `│` : Vertical connection
- `─` : Horizontal connection
- `▼` : Data flow direction
- `┌┐└┘├┤┬┴┼` : Box borders
- `[Box]` : Component/Module
- `•` : List item

---

*Visual Architecture for AI-Based Fake Job Offer Detection System*
*with Threat Intelligence Feature*
