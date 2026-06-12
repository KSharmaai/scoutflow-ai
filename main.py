#!/usr/bin/env python3
"""
ScoutFlow AI - Streamlit Frontend Dashboard
Interactive interface for demonstrating the autonomous compliance audit system

Features:
- Real-time compliance analysis
- Step-by-step reasoning visualization
- Professional email draft generation
- Conflict detection and alerts
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.compliance import ComplianceAgent, ComplianceStatus

# Page configuration
st.set_page_config(
    page_title="ScoutFlow AI - Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .athlete-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-bottom: 20px;
    }
    .status-good {
        background: #d4edda;
        border-left-color: #28a745;
    }
    .status-warning {
        background: #fff3cd;
        border-left-color: #ffc107;
    }
    .status-critical {
        background: #f8d7da;
        border-left-color: #dc3545;
    }
    .reasoning-step {
        background: #f0f2f5;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    .thought {
        border-left-color: #667eea;
        background: #ede7f6;
    }
    .evaluating {
        border-left-color: #ffc107;
        background: #fff8e1;
    }
    .action {
        border-left-color: #28a745;
        background: #e8f5e9;
    }
    .violation {
        border-left-color: #dc3545;
        background: #ffebee;
    }
    .email-draft {
        background: #f5f5f5;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #ddd;
        font-family: Georgia, serif;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)


def load_athlete_data():
    """Load athlete profile from syllabus_deadlines.json"""
    try:
        with open("data/syllabus_deadlines.json", "r") as f:
            data = json.load(f)
        return data["student"]
    except Exception as e:
        st.error(f"Error loading athlete data: {e}")
        return None


def format_reasoning_log(reasoning_log):
    """Format reasoning log entries with color coding."""
    formatted = []
    for entry in reasoning_log:
        if "[THOUGHT]" in entry:
            formatted.append(f"💭 {entry}")
        elif "[EVALUATING]" in entry:
            formatted.append(f"🔍 {entry}")
        elif "[ACTION]" in entry:
            formatted.append(f"✅ {entry}")
        else:
            formatted.append(entry)
    return formatted


def display_athlete_status(athlete):
    """Display athlete status card."""
    html = f"""
    <div class="athlete-card">
        <h3>👤 Athlete Profile</h3>
        <p><strong>Name:</strong> {athlete['name']}</p>
        <p><strong>ID:</strong> {athlete['id']}</p>
        <p><strong>Major:</strong> {athlete['major']}</p>
        <p><strong>Graduation:</strong> {athlete['graduation_year']}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_compliance_status(status):
    """Display compliance status with appropriate styling."""
    if status.alert_flag:
        if status.violation_level == "severe":
            status_class = "status-critical"
            icon = "🚨"
            level_text = "CRITICAL"
        elif status.violation_level == "major":
            status_class = "status-warning"
            icon = "⚠️"
            level_text = "MAJOR"
        else:
            status_class = "status-warning"
            icon = "⚠️"
            level_text = "WARNING"
    else:
        status_class = "status-good"
        icon = "✅"
        level_text = "COMPLIANT"

    html = f"""
    <div class="athlete-card {status_class}">
        <h3>{icon} Compliance Status</h3>
        <p><strong>Level:</strong> {level_text}</p>
        <p><strong>Violations:</strong> {len(status.violations)}</p>
        <p><strong>Conflicts:</strong> {len(status.conflicts)}</p>
        <p><strong>Last Updated:</strong> {status.timestamp}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def display_violations(status):
    """Display identified violations."""
    if not status.violations:
        return
    
    st.subheader("🚨 Violations Detected")
    for i, violation in enumerate(status.violations, 1):
        with st.expander(f"Violation {i}: {violation.get('type', 'Unknown')}", expanded=True):
            st.json(violation)


def display_conflicts(status):
    """Display identified conflicts."""
    if not status.conflicts:
        return
    
    st.subheader("⚠️ Academic-Athletic Conflicts")
    for i, conflict in enumerate(status.conflicts, 1):
        with st.expander(f"Conflict {i}: {conflict.get('type', 'Unknown')}", expanded=True):
            st.warning(conflict.get('type', 'Unknown'))
            
            if conflict['type'] == 'EXAM_TRAVEL_CONFLICT':
                st.write(f"**Course:** {conflict['course']}")
                st.write(f"**Exam:** {conflict['exam']}")
                st.write(f"**Exam Date:** {conflict['exam_date']}")
                st.write(f"**Tournament Dates:** {conflict['tournament_dates']}")
            
            st.json(conflict)


def display_email_draft(course_code):
    """Display and copy email draft."""
    try:
        email_path = Path("data/output") / f"accommodation_request_{course_code}.json"
        if email_path.exists():
            with open(email_path, "r") as f:
                email_data = json.load(f)
            
            st.markdown("### 📧 Professional Accommodation Request Email")
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**To:** Prof. {email_data['instructor']}")
                st.markdown(f"**Subject:** {email_data['subject_line']}")
            with col2:
                if st.button(f"📋 Copy {course_code}", key=f"copy_{course_code}"):
                    st.session_state[f"copied_{course_code}"] = True
                    st.success("✅ Copied to clipboard!")
            
            st.markdown('<div class="email-draft">', unsafe_allow_html=True)
            st.text(email_data['email_body'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show raw JSON
            with st.expander("View JSON"):
                st.json(email_data)
    
    except FileNotFoundError:
        pass


def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 ScoutFlow AI - Dashboard</h1>
        <p>Autonomous Student-Athlete Productivity & Compliance Tracking Agent</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Select View:",
            ["Dashboard", "Analysis Details", "Email Drafts", "About"]
        )
    
    # Load athlete data
    athlete = load_athlete_data()
    if not athlete:
        st.error("Failed to load athlete data")
        return
    
    # Page: Dashboard
    if page == "Dashboard":
        dashboard_page(athlete)
    
    # Page: Analysis Details
    elif page == "Analysis Details":
        analysis_details_page()
    
    # Page: Email Drafts
    elif page == "Email Drafts":
        email_drafts_page()
    
    # Page: About
    elif page == "About":
        about_page()


def dashboard_page(athlete):
    """Main dashboard page."""
    st.write("")
    
    # Display athlete profile
    col1, col2 = st.columns(2)
    with col1:
        display_athlete_status(athlete)
    
    with col2:
        # Display current status placeholder
        st.markdown("""
        <div class="athlete-card">
            <h3>📊 Quick Stats</h3>
            <p><strong>Current Semester:</strong> Summer 2026</p>
            <p><strong>Courses:</strong> 2 Active</p>
            <p><strong>Next Exam:</strong> June 15, 2026</p>
            <p><strong>Athletic Event:</strong> Championship Tournament</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Audit Button Section
    st.markdown("---")
    st.subheader("🔍 Compliance Audit")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        audit_button = st.button(
            "🚀 Run Autonomous Compliance Audit",
            key="audit_button",
            use_container_width=True
        )
    
    # Run audit if button clicked
    if audit_button:
        with st.spinner("⏳ Running comprehensive compliance audit..."):
            # Initialize session state for results
            agent = ComplianceAgent(data_dir="data")
            status = agent.run_pipeline()
            
            # Store in session state
            st.session_state.audit_status = status
            st.session_state.reasoning_log = agent.reasoning_log
            st.session_state.violations = agent.violations
            st.session_state.conflicts = agent.conflicts
        
        st.success("✅ Audit Complete!")
    
    # Display results if available
    if "audit_status" in st.session_state:
        st.write("")
        st.markdown("---")
        
        status = st.session_state.audit_status
        
        # Display compliance status
        display_compliance_status(status)
        
        # Display recommendation
        st.info(status.recommendation)
        
        # Show reasoning steps
        st.markdown("### 📝 Step-by-Step Reasoning Log")
        
        with st.expander("View Detailed Reasoning", expanded=False):
            reasoning_log = st.session_state.reasoning_log
            
            # Create tabs for different step types
            tab1, tab2, tab3 = st.tabs(["All Steps", "Thoughts", "Actions"])
            
            with tab1:
                for entry in reasoning_log:
                    if "[THOUGHT]" in entry:
                        st.markdown(f'<div class="reasoning-step thought">💭 {entry}</div>', 
                                  unsafe_allow_html=True)
                    elif "[EVALUATING]" in entry:
                        st.markdown(f'<div class="reasoning-step evaluating">🔍 {entry}</div>', 
                                  unsafe_allow_html=True)
                    elif "[ACTION]" in entry:
                        st.markdown(f'<div class="reasoning-step action">✅ {entry}</div>', 
                                  unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="reasoning-step">{entry}</div>', 
                                  unsafe_allow_html=True)
            
            with tab2:
                thoughts = [e for e in reasoning_log if "[THOUGHT]" in e]
                for thought in thoughts:
                    st.markdown(f'<div class="reasoning-step thought">💭 {thought}</div>', 
                              unsafe_allow_html=True)
            
            with tab3:
                actions = [e for e in reasoning_log if "[ACTION]" in e]
                for action in actions:
                    st.markdown(f'<div class="reasoning-step action">✅ {action}</div>', 
                              unsafe_allow_html=True)
        
        # Display violations and conflicts
        if status.violations:
            display_violations(status)
        
        if status.conflicts:
            display_conflicts(status)
            
            # Show warning alert
            st.markdown("---")
            st.error("⚠️ **Critical Action Required**: Academic-athletic scheduling conflicts detected. "
                    "Contact professors to arrange accommodations.")
        
        # Show generated email drafts
        if status.conflicts:
            st.markdown("---")
            st.markdown("### 📧 Generated Email Drafts")
            
            # Extract affected courses from conflicts
            affected_courses = set()
            for conflict in status.conflicts:
                if 'course' in conflict:
                    affected_courses.add(conflict['course'])
            
            for course_code in affected_courses:
                st.markdown(f"#### {course_code}")
                display_email_draft(course_code)
        
        # Display raw JSON
        with st.expander("View Raw Compliance Status JSON"):
            st.json({
                "timestamp": status.timestamp,
                "student_id": status.student_id,
                "student_name": status.student_name,
                "alert_flag": status.alert_flag,
                "violation_level": status.violation_level,
                "violations": status.violations,
                "conflicts": status.conflicts,
                "remediation_actions": status.remediation_actions,
                "recommendation": status.recommendation
            })


def analysis_details_page():
    """Detailed analysis page."""
    st.title("📊 Analysis Details")
    
    if "audit_status" not in st.session_state:
        st.info("Run the compliance audit on the Dashboard to view analysis details.")
        return
    
    status = st.session_state.audit_status
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Violations", len(status.violations), 
                 "🚨" if status.violations else "✅")
    
    with col2:
        st.metric("Conflicts", len(status.conflicts),
                 "⚠️" if status.conflicts else "✅")
    
    st.markdown("---")
    
    # Violations details
    if status.violations:
        st.subheader("Violation Details")
        for i, violation in enumerate(status.violations, 1):
            with st.expander(f"Violation {i}: {violation.get('type')}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Type:** {violation.get('type')}")
                    st.write(f"**Severity:** {violation.get('severity')}")
                with col2:
                    st.json(violation)
    else:
        st.success("✅ No violations detected")
    
    st.markdown("---")
    
    # Conflicts details
    if status.conflicts:
        st.subheader("Conflict Details")
        for i, conflict in enumerate(status.conflicts, 1):
            with st.expander(f"Conflict {i}: {conflict.get('type')}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Type:** {conflict.get('type')}")
                    st.write(f"**Severity:** {conflict.get('severity')}")
                with col2:
                    st.json(conflict)
    else:
        st.success("✅ No conflicts detected")
    
    st.markdown("---")
    
    # Remediation actions
    if status.remediation_actions:
        st.subheader("Remediation Actions")
        for i, action in enumerate(status.remediation_actions, 1):
            st.write(f"{i}. {action}")


def email_drafts_page():
    """Email drafts display page."""
    st.title("📧 Email Drafts")
    
    if "audit_status" not in st.session_state:
        st.info("Run the compliance audit on the Dashboard to generate email drafts.")
        return
    
    status = st.session_state.audit_status
    
    # Extract affected courses
    affected_courses = set()
    for conflict in status.conflicts:
        if 'course' in conflict:
            affected_courses.add(conflict['course'])
    
    if not affected_courses:
        st.info("No email drafts generated. No academic-athletic conflicts detected.")
        return
    
    st.write(f"**Generated Accommodation Request Emails:** {len(affected_courses)}")
    st.write("")
    
    for course_code in sorted(affected_courses):
        st.markdown(f"## {course_code}")
        display_email_draft(course_code)
        st.markdown("---")


def about_page():
    """About page."""
    st.title("ℹ️ About ScoutFlow AI")
    
    st.markdown("""
    ## 🎯 Mission
    ScoutFlow AI is an autonomous agent designed to help student-athletes navigate the complex 
    intersection of rigorous academics and competitive athletics while maintaining compliance 
    with NCAA regulations.
    
    ## 🏗️ Architecture
    
    ### Three-Step Reasoning Pipeline (Microsoft Foundry-Inspired)
    
    1. **Context Parsing**: Extract schedule information from unstructured communications
    2. **Constraint Verification**: Validate against NCAA CARA regulations and academic calendars
    3. **Remediation & Action Synthesis**: Generate professional accommodations and alerts
    
    ## 📊 Data Sources
    
    - **messy_schedule.txt**: Unstructured coach communications
    - **syllabus_deadlines.json**: Academic course information and deadlines
    - **compliance_rules.json**: NCAA CARA regulation thresholds
    
    ## 🎓 Use Cases
    
    - Detect practice hour violations (daily/weekly limits)
    - Identify exam-travel conflicts
    - Auto-generate professional accommodation request emails
    - Provide compliance-aligned recommendations
    
    ## 🏆 Built for Microsoft Agents League Hackathon 2026
    
    **Key Features:**
    - Transparent multi-step reasoning with explicit logging
    - Structured JSON compliance status reports
    - Professional email generation
    - Real-time dashboard visualization
    
    ## 📧 Contact
    
    Built by Team ScoutFlow for the Microsoft Agents League Hackathon
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Data Files", 3)
    with col2:
        st.metric("Reasoning Steps", 3)
    with col3:
        st.metric("Compliance Rules", 10)


if __name__ == "__main__":
    main()
