# ScoutFlow AI 🚀

<div style="background:linear-gradient(90deg,#004578,#0078d4);padding:12px;border-radius:8px;margin-bottom:12px;text-align:center;">
  <a href="./AGENTS_LEAGUE_SUBMISSION.html" style="color:#fff;font-weight:700;text-decoration:none;font-family:Segoe UI, system-ui, sans-serif;">Open Official Agents League Submission Guide →</a>
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
- Extracts unstructured data from `messy_schedule.txt` (chaotic coach emails)
- Parses practice hours, flight confirmations, tournament dates
- Converts raw text into structured temporal objects
- **Output:** Cleaned schedule metadata with exact calendar times

### **Step 2: Constraint Verification**
- Cross-references parsed hours against `compliance_rules.json` (NCAA CARA thresholds)
- Checks daily limits (4 hours max, 3.5 hour warning)
- Checks weekly limits (20 hours max, 18 hour warning)
- Queries `syllabus_deadlines.json` for exam dates
- **Detects:** Exam-travel conflicts, daily/weekly violations, rest day violations
- **Output:** Structured violation and conflict reports

### **Step 3: Remediation & Action Synthesis**
- Generates remediation actions for each violation
- **Auto-generates professional accommodation request emails** to professors
- Creates structured JSON compliance status report
- Provides actionable recommendations
- **Output:** Email drafts, JSON status, alert flags

---

## 📊 What We've Built

### **1. Mock Data Layer** (`/data`)
```
data/
├── messy_schedule.txt              # Unstructured coach email
│   └── Flight changes, practice extensions, compliance deadlines
├── syllabus_deadlines.json         # Academic calendar
│   └── 2 courses, exam dates (including critical June 22 conflict)
├── compliance_rules.json           # NCAA CARA regulations
│   └── Daily/weekly limits, thresholds, violations, penalties
└── output/                         # Generated outputs
    ├── compliance_status.json
    ├── accommodation_request_BUS-301.json
    └── accommodation_request_MATH-215.json
```

### **2. Compliance Reasoning Engine** (`src/agents/compliance.py`)

**ComplianceAgent Class** with:
- `_parse_schedule()` - Step 1: Extract dates and practice hours
- `_verify_constraints()` - Step 2: Check violations and conflicts
- `_synthesize_remediation()` - Step 3: Generate emails and recommendations
- Explicit logging with `[THOUGHT]`, `[EVALUATING]`, `[ACTION]` prefixes for judge visibility

**Example Output:**
```
[THOUGHT] Parsing unstructured email text for schedule information...
[EVALUATING] Found flight times: ['6:30 AM', '2:45 PM']
[ACTION] Extracted flight confirmation: DELTA-7849KL
[EVALUATING] Checking Monday: 3 hours
[ACTION] ⚠️ WARNING: Monday approaching daily limit (4.5h > 3.5h warning)
🚨 CRITICAL CONFLICT: BUS-301 Midterm Exam on 2026-06-22 during championship tournament
```

### **3. Streamlit Frontend Dashboard** (`main.py`)

Interactive web interface with:
- **Dashboard Page**
  - Athlete profile card
  - Compliance status display (alert flag, violations, conflicts count)
  - One-click "Run Autonomous Compliance Audit" button
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

- **About Page**
  - Mission statement
  - Architecture overview
  - Use cases and features

### **4. Setup Script** (`setup_mock_data.py`)

Programmatic data generator:
- Auto-creates `/data` directory
- Generates all three mock files
- Can be run independently: `python setup_mock_data.py`

---

## 🎯 Key Features Demonstrated

### ✅ **Multi-Step Reasoning Transparency**
- Judges can see **exactly** what the agent is thinking at each stage
- Three distinct reasoning markers: `[THOUGHT]`, `[EVALUATING]`, `[ACTION]`
- Complete reasoning log preserved and displayable

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
- Compliance-aligned language
- JSON export for integration

### ✅ **Interactive Dashboard**
- Real-time compliance audit execution
- Color-coded alerts (green/yellow/red)
- Expandable reasoning steps
- Easy copy-to-clipboard for emails

---

## 🚀 Project Structure

```
scoutflow-ai/
├── main.py                         # Streamlit frontend dashboard
├── setup_mock_data.py              # Mock data generator script
├── src/
│   └── agents/
│       └── compliance.py           # Core ComplianceAgent reasoning engine
├── data/
│   ├── messy_schedule.txt          # Unstructured coach email
│   ├── syllabus_deadlines.json     # Academic calendar
│   ├── compliance_rules.json       # NCAA CARA regulations
│   └── output/                     # Generated compliance status & emails
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

---

## 🛠️ Installation & Quick Start

### Prerequisites
- Python 3.9+
- pip

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KSharmaai/scoutflow-ai.git
   cd scoutflow-ai
   ```

2. **Create mock data:**
   ```bash
   python setup_mock_data.py
   ```
   Output:
   ```
   ✓ Data directory ready: data
   ✓ Created: data/messy_schedule.txt
   ✓ Created: data/syllabus_deadlines.json
   ✓ Created: data/compliance_rules.json
   ✓ All mock data files created successfully!
   ```

3. **Run the reasoning engine (command line):**
   ```bash
   python src/agents/compliance.py
   ```
   This will:
   - Execute all three reasoning steps
   - Print intermediate thoughts to console
   - Generate compliance status JSON
   - Create professional email drafts

4. **Launch the interactive dashboard:**
   ```bash
   pip install streamlit
   streamlit run main.py
   ```
   - Opens at `http://localhost:8501`
   - Click "Run Autonomous Compliance Audit"
   - View reasoning logs, conflicts, and generated emails

---

## 📋 What the Agent Detects

### **Compliance Violations**
- ✗ Daily practice hours exceed 4-hour NCAA CARA limit
- ✗ Weekly practice hours exceed 20-hour NCAA CARA limit
- ✗ Insufficient rest between training sessions
- ✗ Mandatory rest day requirements not met

### **Academic-Athletic Conflicts**
- ✗ Exams during mandatory tournament travel
- ✗ Exams within 48 hours of travel dates
- ✗ Course schedule overlaps with athletic events

### **Remediation Actions Generated**
- ✓ Reduce practice hours to compliant levels
- ✓ Redistribute weekly schedule
- ✓ Request exam accommodation from professors
- ✓ Auto-generated professional accommodation emails

---

## 📊 Example Output

### **Compliance Status JSON**
```json
{
  "timestamp": "2026-06-12T05:05:10",
  "student_id": "SC-2024-08421",
  "student_name": "Sarah Chen",
  "alert_flag": true,
  "violation_level": "major",
  "violations": [
    {
      "type": "WEEKLY_HOURS_VIOLATION",
      "total_hours": 19.5,
      "limit": 20,
      "severity": "MAJOR"
    }
  ],
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
    "Request exam accommodation for BUS-301 Midterm Exam (scheduled 2026-06-22)...",
    "Redistribute weekly practice hours from 19.5h to maximum 20h..."
  ],
  "recommendation": "🚨 URGENT ACTION REQUIRED..."
}
```

### **Generated Email Draft**
```
Dear Professor Wong,

I am writing to request a potential accommodation for the Midterm Exam 
scheduled for 2026-06-22 in BUS-301.

Due to my participation in our university's championship tournament competition, 
I am required to travel from June 20-23, 2026, as part of my athletic scholarship 
commitment. This mandatory team travel unfortunately overlaps with the Midterm Exam date.

I would like to discuss the possibility of:
1. Taking an early exam before June 20th, or
2. Taking a make-up exam after my return on June 24th, or
3. An alternative assessment method approved by the university

Best regards,
Sarah Chen
Student ID: SC-2024-08421
```

---

## 🎥 Demo Guide (3-Minute Presentation)

1. **[0:00-0:15]** Show dashboard with athlete profile
2. **[0:15-0:30]** Click "Run Autonomous Compliance Audit" button
3. **[0:30-1:30]** Show loading spinner → Reveal reasoning log
   - Expand `[THOUGHT]` steps
   - Show `[EVALUATING]` constraint checks
   - Display `[ACTION]` outcomes
4. **[1:30-2:00]** Show violations and conflicts detected
5. **[2:00-2:30]** Display warning alert: "⚠️ Academic-athletic conflicts detected"
6. **[2:30-3:00]** Show generated email draft → Click copy button → Success message

---

## 🏆 Why This Matters for Hackathon Judges

### ✨ **Transparent Multi-Step Reasoning**
Every decision is logged and visible. Judges can see exactly how the agent:
1. Parsed unstructured data
2. Applied constraint logic
3. Synthesized remediation

### ✨ **Real-World Problem Solving**
Solves an authentic NCAA compliance and academic scheduling problem that affects thousands of student-athletes.

### ✨ **Production-Ready Architecture**
- Structured data models
- Modular reasoning steps
- Professional output formatting
- Interactive visualization

### ✨ **Extensibility**
Easy to integrate with:
- Real M365 Outlook calendars
- Actual NCAA compliance databases
- University registrar systems
- Email delivery services

---

## 👥 Built By

**Kuldeep Sharma** for the Microsoft Agents League Hackathon 2026

**GitHub:** [@KSharmaai](https://github.com/KSharmaai)

---

## 📄 License

MIT License - Feel free to fork, modify, and extend for your institution

---

## 🔗 Resources

- [NCAA CARA Rules](https://www.ncaa.org)
- [Microsoft Foundry Documentation](https://microsoft.com)
- [Streamlit Documentation](https://streamlit.io)
- [Python Agents Architecture](https://github.com/microsoft)

---

**Last Updated:** June 12, 2026  
**Status:** ✅ Complete & Demo-Ready
