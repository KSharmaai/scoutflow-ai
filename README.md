# ScoutFlow AI 🚀

<!-- Replace HTidtcjJvFc with your actual video ID -->
[![Watch the ScoutFlow AI Demo](https://youtu.be/HTidtcjJvFc)

<div style="background:linear-gradient(90deg,#004578,#0078d4);padding:12px;border-radius:8px;margin-bottom:12px;text-align:center;">
  <a href="https://ksharmaai.github.io/scoutflow-ai/AGENTS_LEAGUE_SUBMISSION.html" style="color:#fff;font-weight:700;text-decoration:none;font-family:Segoe UI, system-ui, sans-serif;" target="_blank">Open Official Agents League Submission Guide →</a>
</div>

**Navigation Index:** [Architecture & Flow](docs/ARCHITECTURE.md)

### Autonomous Student-Athlete Productivity & Compliance Tracking Agent
**Built for the Microsoft Agents League Hackathon 2026** | **Track:** Reasoning Agents  
**Core Technologies:** Python, Microsoft Foundry-inspired Architecture, NCAA CARA Compliance

---

## 💡 Inspiration & Problem Statement

Student-athletes live on a knife's edge—balancing rigorous training sessions, cross-country athletic travel, and demanding academic coursework. When a team flight gets delayed or an unexpected practice schedule shift occurs, critical information gets lost in manual communication channels. Academic deadlines collide with tournament dates. Practice hour regulations get violated unknowingly.

**ScoutFlow AI** solves this systemic gap. It is an autonomous multi-step reasoning agent that acts as a proactive co-pilot for:
- 🏫 Academic advisors
- 🏆 Athletic departments
- 🎓 Student-athletes

The agent **transparently** identifies compliance violations and scheduling conflicts, then **autonomously** generates professional accommodation request emails—all with explicit, judge-visible reasoning at every step.

---

## 🧠 Core Architecture: Three-Step Reasoning Pipeline

ScoutFlow AI implements a **deterministic, Foundry-inspired reasoning orchestration** with three distinct steps:

### **Step 1: Context Parsing**
- Extracts unstructured data from `messy_schedule.txt` (chaotic coach emails).
- Parses practice hours, flight confirmations, tournament dates.
- **Dynamically detects hidden mandatory events** (e.g., "Film Review" 7-9 PM → 2.0 hours) throughout entire schedule text.
- Converts raw text into structured temporal objects.
- **Output:** Cleaned schedule metadata with exact calendar times and all parsed event categories.

### **Step 2: Constraint Verification**
- Cross-references **dynamically aggregated** practice hours against `compliance_rules.json` (NCAA CARA thresholds).
- Applies per-category multipliers (Mon-Thu × 4, Friday × 1, Conditioning × 3) to compute weekly totals from parsed events.
- Checks daily limits (4 hours max, 3.5 hour warning).
- Checks weekly limits (20 hours max, 18 hour warning).
- **Validates school-specific rules:** No practice/travel before 7:00 AM, minimum 4-hour rest between sessions.
- Queries `syllabus_deadlines.json` for exam dates.
- **Detects:** Exam-travel conflicts, daily/weekly violations, rest day violations, institutional boundary breaches.
- **Output:** Structured violation and conflict reports with severity ratings.

### **Step 3: Remediation & Action Synthesis**
- Generates remediation actions for each violation.
- **Auto-generates professional accommodation request emails** to professors.
- Creates structured JSON compliance status report.
- Provides actionable recommendations.
- **Output:** Email drafts, JSON status, alert flags.

---

## 📊 What We've Built

### **1. Mock Data Layer** (`/data`)
```text
data/
├── messy_schedule.txt              # Unstructured coach email
│   └── Flight changes, practice extensions, compliance deadlines
├── syllabus_deadlines.json         # Academic calendar
│   └── 2 courses, exam dates (including critical June 22 conflict)
├── compliance_rules.json           # NCAA CARA regulations
│   └── Daily/weekly limits, thresholds, violations, penalties
└── output/                         # Generated outputs
    ├── compliance_status.json
    └── accommodation_request_BUS-301.json
```

### **2. Compliance Reasoning Engine** (`src/agents/compliance.py`)

**ComplianceAgent Class** with:
- `_parse_schedule()` - Step 1: Extract dates and practice hours
- `_verify_constraints()` - Step 2: Check violations and conflicts
- `_synthesize_remediation()` - Step 3: Generate emails and recommendations
- Explicit logging with `[THOUGHT]`, `[EVALUATING]`, `[ACTION]` prefixes for judge visibility.

**Example Output:**
```text
[THOUGHT] Parsing unstructured email text for schedule information...
[EVALUATING] Found flight times: ['6:30 AM', '2:45 PM']
[ACTION] Extracted flight confirmation: DELTA-7849KL
[EVALUATING] Checking Monday: 3 hours
[ACTION] ⚠️ WARNING: Monday approaching daily limit (4.5h > 3.5h warning)
🚨 CRITICAL CONFLICT: BUS-301 Midterm Exam on 2026-06-22 during championship tournament
```

### **3. Streamlit Frontend Dashboard** (`main.py`)

Interactive web interface built using an enterprise-grade **Microsoft Fluent Design Palette**:
- **Dashboard Page**
  - Athlete profile card
  - Compliance status display (alert flag, violations, conflicts count)
  - One-click "Execute Autonomous Compliance Audit" button
  - Loading spinner during execution
  - Step-by-step reasoning log viewer (tabbed interface)
  - Violation/conflict expandable details
  - Professional email draft display with copy-to-clipboard

- **Analysis Details Page**
  - Violation breakdown metrics
  - Conflict analysis with severity badges
  - Remediation actions list

- **Email Drafts Page**
  - All generated accommodation request emails
  - Professional formatting with professor name, subject line, body
  - Copy-to-clipboard functionality per course

---

## 🎯 Key Features Demonstrated

### ✅ **Transparent Multi-Step Reasoning**
- Judges can see **exactly** what the agent is thinking at each stage
- Three distinct reasoning markers: `[THOUGHT]`, `[EVALUATING]`, `[ACTION]`
- Complete reasoning log preserved and displayable

### ✅ **Dynamic Schedule Parsing with Hidden Event Detection**
- Extracts not only explicit practice blocks but also hidden mandatory events (Film Review, Required Attendance).
- Parses time ranges to calculate event duration (e.g., "7-9 PM" → 2.0 hours).
- Applies intelligent multipliers to compute accurate weekly aggregations.

### ✅ **School-Specific Enterprise Governance**
- Validates institutional restrictions (e.g., "No practice before 7:00 AM", "12-hour rest between sessions").
- Flags violations like 6:30 AM flights against school travel boundaries.
- Reads governance rules from `compliance_rules.json` `school_specific_rules` object.

### ✅ **NCAA CARA Compliance Validation**
- **Daily limits:** 4 hours max, 3.5 hour warning threshold
- **Weekly limits:** 20 hours max, 18 hour warning threshold
- Automatic violation detection and severity classification

### ✅ **Academic-Athletic Conflict Detection**
- Identifies exams occurring during tournament travel
- Flags exams within 48 hours of travel
- Severity levels: CRITICAL, HIGH, MAJOR, WARNING

### ✅ **Autonomous Email Generation**
- Professional accommodation request templates
- Personalized with student/course/exam information
- Compliance-aligned language with strict honorific logic check (`Dear Dr. Wong,`)
- JSON export for integration

---

## 🚀 Project Structure

```text
scoutflow-ai/
├── .streamlit/
│   └── config.toml                 # Streamlit client and server configuration
├── main.py                         # Streamlit frontend dashboard
├── setup_mock_data.py              # Mock data generator script
├── AGENTS_LEAGUE_SUBMISSION.html   # Official standalone league submission brief
├── docs/
│   ├── ARCHITECTURE.md             # Core system design blueprint & data flow
│   ├── DEMO_SCRIPT.md              # 60-second video walkthrough narration script
│   └── SUBMISSION_SLIDE.png        # High-resolution native presentation slide
├── src/
│   └── agents/
│       └── compliance.py           # Core ComplianceAgent reasoning engine
├── data/
│   ├── messy_schedule.txt          # Unstructured coach email
│   ├── syllabus_deadlines.json     # Academic calendar
│   ├── compliance_rules.json       # NCAA CARA regulations
│   └── output/                     # Generated compliance status & emails
├── tests/
│   ├── test_compliance.py          # Framework functionality testing
    └── test_output_schema.py       # Data integrity contract testing
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

---

## 🛠️ Installation & Local Quick Start

Follow these steps to deploy and execute ScoutFlow AI locally on your development machine.

### Prerequisites
- Python 3.9+
- pip

### Setup & Run Blueprint

1. **Clone the repository and enter workspace:**
   ```bash
   git clone [https://github.com/KSharmaai/scoutflow-ai.git](https://github.com/KSharmaai/scoutflow-ai.git)
   cd scoutflow-ai
   ```

2. **Initialize your virtual environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize mock source data directories:**
   ```bash
   python3 setup_mock_data.py
   ```

5. **Run the local testing matrix:**
   Verify that your local backend engines pass data structure rules before deploying the UI:
   ```bash
   pytest tests/
   ```

6. **Launch the reasoning agent engine directly (CLI Trace Mode):**
   ```bash
   python3 src/agents/compliance.py
   ```

7. **Launch the web-based interactive dashboard:**
   ```bash
   streamlit run main.py --server.port 8080
   ```
   * Open your browser to `http://localhost:8080` to interact with the platform.
   * *Note: If port 8080 is blocked by your system firewall or a background service, override it on launch:* `streamlit run main.py --server.port 8501`

---

## 📋 What the Agent Detects

### **Compliance Violations**
- Daily practice hours exceed 4-hour NCAA CARA limit
- Weekly practice hours exceed 20-hour NCAA CARA limit
- Insufficient rest between training sessions
- Mandatory rest day requirements not met

### **Academic-Athletic Conflicts**
- Exams during mandatory tournament travel
- Exams within 48 hours of travel dates
- Course schedule overlaps with athletic events

### **Remediation Actions Generated**
- ✓ Reduce practice hours to compliant levels
- ✓ Redistribute weekly schedule blocks
- ✓ Request exam accommodation from professors
- ✓ Auto-generate professional accommodation emails

---

## 📊 Example Output

### **Compliance Status JSON**
```json
{
  "timestamp": "2026-06-12T21:43:04.284913",
  "student_id": "SC-2024-08421",
  "student_name": "Sarah Chen",
  "alert_flag": true,
  "violation_level": "severe",
  "violations": [],
  "conflicts": [
    {
      "type": "EXAM_TRAVEL_CONFLICT",
      "course": "BUS-301",
      "exam": "Midterm Exam",
      "exam_date": "2026-06-22",
      "tournament_dates": "2026-06-20 to 2026-06-23",
      "severity": "CRITICAL"
    }
  ],
  "remediation_actions": [
    "Request exam accommodation for BUS-301 Midterm Exam (scheduled 2026-06-22) due to mandatory championship tournament travel (2026-06-20 to 2026-06-23). Contact professor immediately."
  ],
  "recommendation": "🚨 URGENT ACTION REQUIRED: Critical exam-travel conflict detected. Contact academic advisor and professors immediately to arrange accommodations. Monitor compliance violations closely."
}
```

### **Generated Email Draft**
```text
Subject: Request for Exam Accommodation - BUS-301 Midterm Exam

Dear Dr. Wong,

I am writing to request a potential accommodation for the Midterm Exam scheduled for 2026-06-22 in BUS-301.

Due to my participation in our university's championship tournament competition, I am required to travel from June 20-23, 2026, as part of my athletic scholarship commitment. This mandatory team travel unfortunately overlaps with the Midterm Exam date.

I understand the importance of maintaining academic integrity and completing all assessments. I would like to discuss the possibility of:
1. Taking an early exam before June 20th, or
2. Taking a make-up exam after my return on June 24th, or
3. An alternative assessment method approved by the university

I have consistently maintained strong academic performance in BUS-301 and am committed to demonstrating my knowledge of the course material in any format you deem appropriate.

I will follow up with your office by end of business tomorrow to confirm your availability to discuss this matter.

Thank you for your understanding and consideration.

Best regards,
Sarah Chen
Student ID: SC-2024-08421
Major: Business Analytics
```

---

## 🎥 Demo Guide (60-Second Walkthrough)

Our video walkthrough follows this strict, high-impact timeline:
- **[0:00 - 0:10]** Platform introduction at the dashboard home view.
- **[0:10 - 0:25]** Click **"Execute Autonomous Compliance Audit"** to trigger live context parsing.
- **[0:25 - 0:45]** Toggle between **Integrated Log Stream** and **Procedural Thoughts** to explore multi-step trace logic.
- **[0:45 - 1:01]** View generated communication templates, verify title-checked greetings (`Dear Dr. Wong,`), and fire copy buffers.

---

## 🏆 Why This Matters for Hackathon Judges

### ✨ **Transparent Multi-Step Reasoning**
Every decision is logged and visible. Judges can see exactly how the agent parses unstructured data, applies constraint logic, and synthesizes remediation.

### ✨ **Real-World Problem Solving**
Solves an authentic NCAA compliance and academic scheduling problem that affects thousands of student-athletes.

### ✨ **Production-Ready Architecture**
Features structured data models, modular reasoning steps, professional output formatting, and an intuitive presentation layout.

---

## 👥 Built By

**Kuldeep Sharma** for the Microsoft Agents League Hackathon 2026

**GitHub:** [@KSharmaai](https://github.com/KSharmaai)

---

## 📄 License

MIT License - Feel free to fork, modify, and extend for your institution

---

**Last Updated:** June 12, 2026  
**Status:** ✅ Complete & Demo-Ready
