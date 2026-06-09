# ScoutFlow AI 🚀
### Autonomous Athlete Productivity & Compliance Tracking Co-Pilot
**Built for the Microsoft Agents League Hackathon 2026** **Track:** Reasoning Agents  
**Core Technologies:** Python, Microsoft Foundry, Microsoft 365 Work IQ  

---

## 💡 Inspiration & Problem Statement
Student-athletes live on a knife’s edge—balancing grueling training sessions, cross-country travel manifests, and rigorous academic workloads. Simultaneously, university athletic departments face immense legal and financial pressure to stay strictly compliant with NCAA and institutional regulations, such as CARA (Countable Athletic Related Activities) hourly limits. 

When a team flight gets delayed or an unexpected practice schedule shift occurs, manual communication channels break down rapidly. What starts as a logistical hurdle quickly cascades into overwhelming academic stress for the athlete and major compliance liability for the university. 

**ScoutFlow AI** bridges this systemic gap. It is an autonomous multi-step reasoning agent that acts as a proactive co-pilot for athletic departments, academic advisors, and student-athletes to track productivity and flag compliance anomalies *before* they become official violations.

---

## ⚙️ Core Architecture & Agentic Workflow
ScoutFlow AI does not rely on simple, context-blind database triggers. Instead, it leverages a powerful **Python** backend orchestrated by **Microsoft Foundry** to execute deterministic, multi-step cognitive reasoning loops:

1. **Ingestion & Sanitation:** Extracts unstructured data payloads (messy coaching text notes, fragmented travel documents, course syllabi text).
2. **Evaluation & Modeling:** Converts raw strings into structured temporal objects, calculating active vs. countable training hours.
3. **Constraint Logic Evaluation:** Validates calculated metrics against localized regulatory parameters (e.g., the NCAA 20-hour weekly CARA threshold).
4. **Autonomous Remediation Routing:** Navigates the organizational graph to propose active scheduling fixes and autogenerate Outlook email exception templates for human-in-the-loop validation.

5. ## 🧠 Microsoft IQ Layer Integration
To achieve deep operational intelligence, ScoutFlow AI integrates seamlessly with the **Microsoft IQ intelligence layer**:

* **Work IQ Integration:** Serves as our agent's structural memory backbone. By securely connecting to the organization's Microsoft 365 Graph (Outlook calendars, emails, Teams channels, and OneDrive document storage), the agent moves beyond siloed data inputs. It dynamically maps out the real-world contextual relationships between athletes, their coaching staff, their specific professors, and their travel timelines.

---

## 🚀 Repository Directory Structure
```text
scoutflow-ai/
├── data/
│   ├── cara_rules.json          # NCAA / Institutional policy configurations
│   └── mock_m365_graph.json     # Mock database representing Outlook/OneDrive context
├── src/
│   ├── __init__.py
│   ├── main.py                  # Main application entry point & console pipeline
│   ├── evaluator.py             # Data sanitation evaluation loop
│   ├── reasoning_engine.py      # Core Microsoft Foundry reasoning orchestrator
│   └── service_layer.py         # Mock M365 Graph/Outlook graph integrations
├── tests/
│   └── test_compliance.py       # Automated unit tests ensuring system reliability
└── requirements.txt             # Project dependencies

## 🛠️ Installation & Execution Guide

### Prerequisites
* Python 3.10 or higher
* Pip package manager

### Setup Instructions
1. Clone this public repository:
   ```bash
   git clone https://github.com/KSharmaai/scoutflow-ai.git
   cd scoutflow-ai
