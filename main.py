#!/usr/bin/env python3
"""
ScoutFlow AI - Streamlit Frontend Dashboard
Interactive interface for demonstrating the autonomous compliance audit system
"""

import streamlit as st
import json
import html
from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.compliance import ComplianceAgent, ComplianceStatus

# Page configuration
st.set_page_config(
    page_title="ScoutFlow AI | Institutional Compliance Workspace",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECT MICROSOFT FLUENT DESIGN PATTERNS (CSS) ---
st.markdown("""
<style>
    /* Global Canvas Styling */
    .stApp {
        background-color: #faf9f8;
        font-family: 'Segoe UI', -apple-system, sans-serif;
    }
    
    /* Professional Header Top Banner */
    .fluent-header {
        background: linear-gradient(90deg, #004578 0%, #0078d4 100%);
        padding: 24px 32px;
        border-radius: 6px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .fluent-header h1 {
        margin: 0;
        font-size: 2.2em;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    .fluent-header p {
        margin: 4px 0 0 0;
        font-size: 1.05em;
        opacity: 0.9;
    }
    
    /* Modern Dashboard Structured Grid Cards */
    .fluent-card {
        background: white;
        padding: 20px;
        border-radius: 4px;
        border: 1px solid #edebe9;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .fluent-card h3 {
        margin-top: 0;
        color: #323130;
        font-size: 1.15em;
        font-weight: 600;
        border-bottom: 1px solid #f3f2f1;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    
    /* Strict Diagnostic Alert Banners */
    .alert-banner {
        padding: 16px;
        border-radius: 4px;
        border: 1px solid #edebe9;
        margin-bottom: 16px;
        font-weight: 500;
    }
    .status-good {
        background: #f3f9f4;
        border-left: 4px solid #107c41;
        color: #107c41;
    }
    .status-warning {
        background: #fffdf6;
        border-left: 4px solid #d83b01;
        color: #d83b01;
    }
    .status-critical {
        background: #fde7e9;
        border-left: 4px solid #a4262c;
        color: #a4262c;
    }
    
    /* Sequential Log Pipeline Architecture */
    .log-box {
        background: white;
        border: 1px solid #edebe9;
        border-radius: 4px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .log-entry {
        font-family: 'Consolas', monospace;
        font-size: 0.88em;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 4px;
        border-left: 3px solid #605e5c;
    }
    .entry-thought { border-left-color: #0078d4; background: #f3f2f1; color: #004578; }
    .entry-evaluating { border-left-color: #ffb900; background: #fffdf6; color: #7a5400; }
    .entry-action { border-left-color: #107c41; background: #f3f9f4; color: #107c41; }
    
    /* High-Contrast Academic Email Shell */
    .email-container {
        background: #ffffff;
        padding: 24px;
        border-radius: 4px;
        border: 1px solid #d2d0ce;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        line-height: 1.6;
        color: #323130;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)


def _sanitize_html(value):
    """Escape text for safe inclusion in HTML blocks."""
    return html.escape(str(value)) if value is not None else ""


def load_athlete_data():
    """Load athlete profile from syllabus_deadlines.json"""
    try:
        with open("data/syllabus_deadlines.json", "r") as f:
            data = json.load(f)
        return data["student"]
    except Exception as e:
        st.error(f"Error loading athlete data: {e}")
        return None


def display_athlete_status(athlete):
    """Display athlete status card."""
    athlete_name = _sanitize_html(athlete.get('name', 'Unknown'))
    athlete_id = _sanitize_html(athlete.get('id', 'Unknown'))
    athlete_major = _sanitize_html(athlete.get('major', 'Unknown'))
    athlete_grad = _sanitize_html(athlete.get('graduation_year', 'Unknown'))

    html = f"""
    <div class="fluent-card">
        <h3>👤 Student-Athlete Profile Information</h3>
        <table style="width:100%; border-collapse:collapse; font-size:0.95em;">
            <tr style="border-bottom: 1px solid #f3f2f1;"><td style="padding:6px 0; color:#605e5c;"><strong>Full Name:</strong></td><td style="text-align:right; font-weight:500;">{athlete_name}</td></tr>
            <tr style="border-bottom: 1px solid #f3f2f1;"><td style="padding:6px 0; color:#605e5c;"><strong>Institutional ID:</strong></td><td style="text-align:right; font-weight:500;">`{athlete_id}`</td></tr>
            <tr style="border-bottom: 1px solid #f3f2f1;"><td style="padding:6px 0; color:#605e5c;"><strong>Academic Major:</strong></td><td style="text-align:right; font-weight:500;">{athlete_major}</td></tr>
            <tr><td style="padding:6px 0; color:#605e5c;"><strong>Graduation Cohort:</strong></td><td style="text-align:right; font-weight:500;">{athlete_grad}</td></tr>
        </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_compliance_status(status):
    """Display compliance status with executive styling."""
    if status.alert_flag:
        if status.violation_level == "severe":
            status_class = "status-critical"
            icon = "🚨"
            level_text = "CRITICAL RISK IDENTIFIED"
        elif status.violation_level == "major":
            status_class = "status-warning"
            icon = "⚠️"
            level_text = "MAJOR BREACH THRESHOLD"
        else:
            status_class = "status-warning"
            icon = "⚠️"
            level_text = "WARNING THRESHOLD ACTIVE"
    else:
        status_class = "status-good"
        icon = "✅"
        level_text = "COMPLIANT STATUS VALIDATED"

    timestamp = _sanitize_html(status.timestamp)
    html = f"""
    <div class="alert-banner {status_class}">
        <span style="font-size:1.2em; margin-right:8px;">{icon}</span> 
        <strong>System Audit Status: {level_text}</strong>
        <div style="font-size:0.88em; font-weight:normal; margin-top:4px; color:#323130;">
            Active Violations: {len(status.violations)} | Detected Graph Conflicts: {len(status.conflicts)} | Timestamp: {timestamp}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_violations(status):
    """Display identified violations."""
    if not status.violations:
        return
    
    st.markdown("### 🚨 Active Compliance Violations")
    for i, violation in enumerate(status.violations, 1):
        with st.expander(f"Violation [{i}]: {violation.get('type', 'Unknown')}", expanded=True):
            st.json(violation)


def display_conflicts(status):
    """Display identified conflicts."""
    if not status.conflicts:
        return
    
    st.markdown("### ⚠️ Mapped Schedule Multi-Source Conflicts")
    for i, conflict in enumerate(status.conflicts, 1):
        with st.expander(f"Conflict [{i}]: {conflict.get('type', 'Unknown')}", expanded=True):
            if conflict['type'] == 'EXAM_TRAVEL_CONFLICT':
                st.error(f"**Structural Intersection Detected:** Exam event occurs inside team tournament travel dates.")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown(f"**Academic Course:** {conflict['course']}")
                    st.markdown(f"**Evaluation Block:** {conflict['exam']}")
                with col_c2:
                    st.markdown(f"**Target Exam Date:** {conflict['exam_date']}")
                    st.markdown(f"**Tournament Travel Window:** {conflict['tournament_dates']}")
            st.json(conflict)


def display_email_draft(course_code):
    """Display and copy email draft."""
    try:
        email_path = Path("data/output") / f"accommodation_request_{course_code}.json"
        if email_path.exists():
            with open(email_path, "r") as f:
                email_data = json.load(f)
            
            st.markdown(" ")
            st.markdown(f"#### ✉️ Accommodation Draft Blueprint: {course_code}")
            
            with st.container():
                col_e1, col_e2 = st.columns([4, 1])
                with col_e1:
                    instructor = _sanitize_html(email_data.get('instructor', 'Unknown'))
                    subject_line = _sanitize_html(email_data.get('subject_line', 'No Subject'))
                    safe_course_code = _sanitize_html(course_code)
                    st.markdown(f"**Recipient Registry:** `Prof. {instructor}`")
                    st.markdown(f"**Subject Line Allocation:** `{subject_line}`")
                with col_e2:
                    if st.button(f"📋 Copy Draft Buffer", key=f"copy_{safe_course_code}", use_container_width=True):
                        st.session_state[f"copied_{safe_course_code}"] = True
                        st.success("Buffer Updated")

                st.markdown('<div class="email-container">', unsafe_allow_html=True)
                st.text(email_data['email_body'])
                st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error compiling communication artifact: {e}")


def main():
    """Main Streamlit application."""
    
    # Header Banner Block
    st.markdown("""
    <div class="fluent-header">
        <h1>ScoutFlow AI</h1>
        <p>Institutional Roster Intelligence & Dynamic Athletic Compliance Orchestration Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Sidebar
    with st.sidebar:
        st.markdown("### 🏛️ Navigation Control")
        page = st.radio(
            "Select Environment View:",
            ["Dashboard Hub", "Detailed Analytics", "Remediation Templates", "System Context"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.markdown("#### 🤖 Operational Engine")
        st.info("Orchestration Framework: **Microsoft Foundry Simulation**\n\nMemory Context Layer: **Work IQ Context Graph**")
    
    athlete = load_athlete_data()
    if not athlete:
        st.error("Terminal initialization failure: Unable to populate core roster data components.")
        return
    
    if page == "Dashboard Hub":
        dashboard_page(athlete)
    elif page == "Detailed Analytics":
        analysis_details_page()
    elif page == "Remediation Templates":
        email_drafts_page()
    elif page == "System Context":
        about_page()


def dashboard_page(athlete):
    """Main dashboard interface."""
    col_dash1, col_dash2 = st.columns(2)
    with col_dash1:
        display_athlete_status(athlete)
    
    with col_dash2:
        st.markdown("""
        <div class="fluent-card">
            <h3>📊 Live Registry Metadata</h3>
            <table style="width:100%; border-collapse:collapse; font-size:0.95em;">
                <tr style="border-bottom: 1px solid #f3f2f1;"><td style="padding:6px 0; color:#605e5c;">Current Term:</td><td style="text-align:right; font-weight:500;">Summer 2026</td></tr>
                <tr style="border-bottom: 1px solid #f3f2f1;"><td style="padding:6px 0; color:#605e5c;">Active Curriculums:</td><td style="text-align:right; font-weight:500;">2 Registered Blocks</td></tr>
                <tr style="border-bottom: 1px solid #f3f2f1;"><td style="padding:6px 0; color:#605e5c;">Target Milestone:</td><td style="text-align:right; font-weight:500;">BUS-301 Midterm (June 22)</td></tr>
                <tr><td style="padding:6px 0; color:#605e5c;">Athletic Window:</td><td style="text-align:right; font-weight:500;">Championship Tournament</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("⚙️ Verification Control Run")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1.2, 1, 1])
    with col_btn1:
        audit_button = st.button("🚀 Execute Autonomous Compliance Audit", type="primary", use_container_width=True)
    
    if audit_button:
        with st.spinner("⏳ Initiating multi-step procedural check via Microsoft Foundry runtime loops..."):
            agent = ComplianceAgent(data_dir="data")
            status = agent.run_pipeline()
            
            st.session_state.audit_status = status
            st.session_state.reasoning_log = agent.reasoning_log
            st.session_state.violations = agent.violations
            st.session_state.conflicts = agent.conflicts
        st.success("System Verification Cycle Complete.")
    
    if "audit_status" in st.session_state:
        st.markdown(" ")
        status = st.session_state.audit_status
        display_compliance_status(status)
        
        st.info(f"💡 **Executive Action Recommendation:** {status.recommendation}")
        
        # Chronological Execution Pipeline Container
        st.markdown("### 🪵 Traceable Pipeline Process History")
        with st.container():
            reasoning_log = st.session_state.reasoning_log
            tab_l1, tab_l2, tab_l3 = st.tabs(["Integrated Log Stream", "Procedural Thoughts", "System Dispatches"])
            
            with tab_l1:
                st.markdown('<div class="log-box">', unsafe_allow_html=True)
                for entry in reasoning_log:
                    if "[THOUGHT]" in entry:
                        st.markdown(f'<div class="log-entry entry-thought">💭 {entry}</div>', unsafe_allow_html=True)
                    elif "[EVALUATING]" in entry:
                        st.markdown(f'<div class="log-entry entry-evaluating">🔍 {entry}</div>', unsafe_allow_html=True)
                    elif "[ACTION]" in entry:
                        st.markdown(f'<div class="log-entry entry-action">✅ {entry}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="log-entry">{entry}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with tab_l2:
                st.markdown('<div class="log-box">', unsafe_allow_html=True)
                for entry in [e for e in reasoning_log if "[THOUGHT]" in e]:
                    st.markdown(f'<div class="log-entry entry-thought">💭 {entry}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab_l3:
                st.markdown('<div class="log-box">', unsafe_allow_html=True)
                for entry in [e for e in reasoning_log if "[ACTION]" in e]:
                    st.markdown(f'<div class="log-entry entry-action">✅ {entry}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        if status.violations:
            display_violations(status)
        
        if status.conflicts:
            display_conflicts(status)
            st.error("🚨 **Immediate Administrative Intervention Mandatory:** Conflicting cross-calendar dependencies detected. Dispatch remediation artifacts immediately.")
            
            st.markdown("---")
            st.markdown("### 📧 Generated Communication Workspace")
            affected_courses = {c['course'] for c in status.conflicts if 'course' in c}
            for course_code in sorted(affected_courses):
                display_email_draft(course_code)


def analysis_details_page():
    """Detailed structural validation reports."""
    st.title("📊 Detailed Diagnostic Metrics")
    
    if "audit_status" not in st.session_state:
        st.info("Awaiting runtime execution tracking parameters. Execute an audit block inside the main dashboard to generate metrics maps.")
        return
    
    status = st.session_state.audit_status
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Identified Rule Deviations", len(status.violations), delta="Severe Breach Risk" if status.violations else None, delta_color="inverse")
    with col_m2:
        st.metric("Graph Dependency Clashes", len(status.conflicts), delta="Intervention Required" if status.conflicts else None, delta_color="inverse")
    
    st.markdown("---")
    if status.violations:
        display_violations(status)
    else:
        st.success("✅ NCAA CARA parameters conform to institutional boundary guidelines.")
        
    st.markdown("---")
    if status.conflicts:
        display_conflicts(status)
    else:
        st.success("✅ Work IQ mapping verified: Zero cross-calendar dependency clashes identified.")
        
    st.markdown("---")
    if status.remediation_actions:
        st.markdown("### 📋 Explicit Mitigation Roadmap")
        for i, action in enumerate(status.remediation_actions, 1):
            st.markdown(f"**{i}.** {action}")


def email_drafts_page():
    """Communication asset dispatch room."""
    st.title("📧 Communication Asset Dispatch Center")
    
    if "audit_status" not in st.session_state:
        st.info("Awaiting structural execution maps. Run compliance audits from the main dashboard context to construct text templates.")
        return
    
    status = st.session_state.audit_status
    affected_courses = {c['course'] for c in status.conflicts if 'course' in c}
    
    if not affected_courses:
        st.success("No active communication templates required: Roster records display zero scheduling clashes.")
        return
        
    st.write(f"**Compiled Institutional Relief Requests:** {len(affected_courses)}")
    for course_code in sorted(affected_courses):
        display_email_draft(course_code)


def about_page():
    """System framework documentation overview."""
    st.title("ℹ️ Technical Specification Overview")
    
    st.markdown("""
    ### 🛡️ System Blueprint & Core Scope
    ScoutFlow AI maps unstructured external communication models directly against rigid operational frameworks 
    (NCAA CARA regulatory boundaries) and structural, multi-layered enterprise databases (M365 Work IQ Roster and Syllabus nodes). 
    The engine abstracts complex temporal sorting problems into high-transparency remediation pipelines.
    
    ### 🧠 Procedural Architecture (Microsoft Foundry Orchestration Design Pattern)
    The system isolates background logic constraints into three deterministic sequence barriers:
    1. **Context Extraction:** Regular expression parsers digest disorganized text blocks to map timestamps into operational JSON values.
    2. **Constraint Check Matrix:** The processing runtime evaluates active metadata arrays against structural boundary ceilings.
    3. **Remediation Protocol Layer:** The system generates structured state logs alongside personalized communication relief drafts.
    
    ---
    ### 🏆 Project Status Report
    * **Target Competition Runtimes:** Microsoft Agents League Developer Arena (June 2026) [cite: 1]
    * **Integrated Data Assets Loading:** `messy_schedule.txt` | `syllabus_deadlines.json` | `compliance_rules.json` [cite: 5, 7, 8, 9]
    * **Development Framework:** Native Python 3 Enterprise Core Implementation [cite: 1]
    """)


if __name__ == "__main__":
    main()