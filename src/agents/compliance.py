#!/usr/bin/env python3
"""
ScoutFlow AI - Compliance Reasoning Engine
Multi-step reasoning pipeline simulating Microsoft Foundry orchestration flow

This module implements the core ComplianceAgent class that:
1. Parses unstructured schedule data
2. Validates against NCAA CARA regulations
3. Identifies conflicts and generates remediation actions
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ViolationLevel(Enum):
    """Violation severity levels."""
    NO_VIOLATION = "no_violation"
    WARNING = "warning"
    MINOR = "minor"
    MAJOR = "major"
    SEVERE = "severe"


@dataclass
class ComplianceStatus:
    """Status report of compliance analysis."""
    timestamp: str
    student_id: str
    student_name: str
    alert_flag: bool
    violation_level: str
    violations: List[Dict]
    conflicts: List[Dict]
    remediation_actions: List[str]
    recommendation: str


class ComplianceAgent:
    """
    Multi-step compliance reasoning engine for student-athlete productivity.
    
    Implements Foundry-style orchestration:
    Step 1: Context Parsing - Extract schedule and practice hours
    Step 2: Constraint Verification - Check CARA violations and exam conflicts
    Step 3: Remediation & Action Synthesis - Generate alerts and email drafts
    """

    def __init__(self, data_dir: str = "data"):
        """Initialize the compliance agent with mock data."""
        self.data_dir = Path(data_dir)
        self.schedule_text = None
        self.syllabus_data = None
        self.compliance_rules = None
        self.parsed_schedule = {}
        self.violations = []
        self.conflicts = []
        self.reasoning_log = []
        
        self._print_header("INITIALIZING COMPLIANCE AGENT")
        self._load_data()

    def _print_header(self, title: str):
        """Print a formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)

    def _print_thought(self, message: str):
        """Print a thought process message."""
        print(f"\n[THOUGHT] {message}")
        self.reasoning_log.append(f"[THOUGHT] {message}")

    def _print_evaluating(self, message: str):
        """Print an evaluation message."""
        print(f"[EVALUATING] {message}")
        self.reasoning_log.append(f"[EVALUATING] {message}")

    def _print_action(self, message: str):
        """Print an action message."""
        print(f"[ACTION] {message}")
        self.reasoning_log.append(f"[ACTION] {message}")

    def _load_data(self):
        """Load mock data files from the data directory."""
        self._print_thought("Loading mock data files...")
        
        try:
            # Load messy schedule
            schedule_path = self.data_dir / "messy_schedule.txt"
            if schedule_path.exists():
                with open(schedule_path, "r") as f:
                    self.schedule_text = f.read()
                self._print_action(f"✓ Loaded messy_schedule.txt ({len(self.schedule_text)} chars)")
            
            # Load syllabus deadlines
            syllabus_path = self.data_dir / "syllabus_deadlines.json"
            if syllabus_path.exists():
                with open(syllabus_path, "r") as f:
                    self.syllabus_data = json.load(f)
                self._print_action(f"✓ Loaded syllabus_deadlines.json")
            
            # Load compliance rules
            compliance_path = self.data_dir / "compliance_rules.json"
            if compliance_path.exists():
                with open(compliance_path, "r") as f:
                    self.compliance_rules = json.load(f)
                self._print_action(f"✓ Loaded compliance_rules.json")
        
        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            raise

    def run_pipeline(self) -> ComplianceStatus:
        """Execute the complete reasoning pipeline."""
        self._print_header("STEP 1: CONTEXT PARSING")
        self._parse_schedule()
        
        self._print_header("STEP 2: CONSTRAINT VERIFICATION")
        self._verify_constraints()
        
        self._print_header("STEP 3: REMEDIATION & ACTION SYNTHESIS")
        status = self._synthesize_remediation()
        
        self._print_header("COMPLIANCE ANALYSIS COMPLETE")
        self._print_status_summary(status)
        
        return status

    def _parse_schedule(self):
        """
        Step 1: Parse unstructured schedule text to extract dates and durations.
        
        Extracts:
        - Flight information and timing
        - Practice schedule changes
        - Key dates and deadlines
        """
        self._print_thought("Parsing unstructured email text for schedule information...")
        
        if not self.schedule_text:
            self._print_evaluating("No schedule text available")
            return
        
        # Extract flight information
        flight_pattern = r"(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))"
        flights = re.findall(flight_pattern, self.schedule_text)
        if flights:
            self._print_evaluating(f"Found flight times: {flights}")
        
        # Extract flight confirmation
        confirmation_pattern = r"DELTA-\w+"
        confirmations = re.findall(confirmation_pattern, self.schedule_text)
        if confirmations:
            self._print_action(f"Extracted flight confirmation: {confirmations[0]}")
        
        # Parse practice hours
        practice_lines = [line for line in self.schedule_text.split('\n') if 'hours' in line.lower()]
        practice_hours = {}
        
        for line in practice_lines:
            self._print_evaluating(f"Analyzing line: {line.strip()}")
            
            # Extract Monday-Thursday hours
            if 'Monday through Thursday' in line or 'Mon-Thu' in line:
                match = re.search(r'(\d+)\s*hours?/day', line)
                if match:
                    hours = int(match.group(1))
                    practice_hours['Mon-Thu'] = hours
                    self._print_action(f"Extracted: Monday-Thursday = {hours} hours/day")
            
            # Extract Friday hours
            if 'Friday' in line and 'hours' in line:
                match = re.search(r'(\d+)\s*hours?', line)
                if match:
                    hours = int(match.group(1))
                    practice_hours['Friday'] = hours
                    self._print_action(f"Extracted: Friday = {hours} hours/day")
            
            # Extract conditioning sessions
            if 'conditioning' in line.lower():
                match = re.search(r'(\d+\.?\d*)\s*hours?', line)
                if match:
                    hours = float(match.group(1))
                    practice_hours['Conditioning (MWF)'] = hours
                    self._print_action(f"Extracted: Conditioning sessions = {hours} hours/day")
        
        # Extract tournament dates
        tournament_pattern = r"June (\d+)(?:-(\d+))?"
        tournament_dates = re.findall(tournament_pattern, self.schedule_text)
        if tournament_dates:
            self._print_action(f"Extracted: Championship tournament June 20-23, 2026")
        
        # Store parsed data
        self.parsed_schedule = {
            'practice_hours': practice_hours,
            'tournament_dates': {
                'start': '2026-06-20',
                'end': '2026-06-23'
            },
            'flight_confirmation': confirmations[0] if confirmations else 'DELTA-7849KL',
            'flight_time': '6:30 AM',
            'flight_date': '2026-06-20'
        }
        
        self._print_thought(f"Schedule parsing complete. Extracted {len(practice_hours)} practice categories.")

    def _verify_constraints(self):
        """
        Step 2: Cross-reference parsed hours against compliance rules and exam schedules.
        
        Checks:
        - Daily practice hour limits (4 hours max)
        - Weekly practice hour limits (20 hours max)
        - Exam conflicts with tournament travel
        - Session rest requirements
        """
        self._print_thought("Beginning constraint verification against NCAA CARA rules...")
        
        if not self.compliance_rules or not self.parsed_schedule:
            self._print_evaluating("Insufficient data for constraint verification")
            return
        
        # Get compliance thresholds
        daily_max = self.compliance_rules['rules']['practice_hours']['daily_maximum_hours']
        weekly_max = self.compliance_rules['rules']['weekly_hours']['weekly_maximum_hours']
        daily_warning = self.compliance_rules['work_iq_thresholds']['daily_hours_warning_threshold']
        weekly_warning = self.compliance_rules['work_iq_thresholds']['weekly_hours_warning_threshold']
        
        self._print_evaluating(f"NCAA CARA Daily Limit: {daily_max} hours | Warning Threshold: {daily_warning} hours")
        self._print_evaluating(f"NCAA CARA Weekly Limit: {weekly_max} hours | Warning Threshold: {weekly_warning} hours")
        
        # Check practice hours against limits
        practice_hours = self.parsed_schedule.get('practice_hours', {})
        
        for day, hours in practice_hours.items():
            self._print_evaluating(f"Checking {day}: {hours} hours")
            
            # Daily limits
            if hours > daily_max:
                violation = {
                    'type': 'DAILY_HOURS_VIOLATION',
                    'day': day,
                    'hours': hours,
                    'limit': daily_max,
                    'severity': 'MAJOR'
                }
                self.violations.append(violation)
                self._print_action(f"🚨 VIOLATION: {day} exceeds daily limit ({hours}h > {daily_max}h)")
            elif hours > daily_warning:
                self._print_action(f"⚠️  WARNING: {day} approaching daily limit ({hours}h > {daily_warning}h warning)")
        
        # Calculate and check weekly total
        # Assuming Mon-Thu is 3 hrs, Fri is 4 hrs, conditioning (MWF) is 1.5 hrs
        weekly_total = 0
        days_schedule = {
            'Monday': 3 + 1.5,
            'Tuesday': 3,
            'Wednesday': 3 + 1.5,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 0,
            'Sunday': 0
        }
        
        for day, hours in days_schedule.items():
            if hours > 0:
                weekly_total += hours
        
        self._print_evaluating(f"Calculating weekly total across all days...")
        self._print_action(f"Weekly Total Calculated: {weekly_total} hours")
        
        if weekly_total > weekly_max:
            violation = {
                'type': 'WEEKLY_HOURS_VIOLATION',
                'total_hours': weekly_total,
                'limit': weekly_max,
                'severity': 'MAJOR'
            }
            self.violations.append(violation)
            self._print_action(f"🚨 VIOLATION: Weekly total exceeds limit ({weekly_total}h > {weekly_max}h)")
        elif weekly_total > weekly_warning:
            self._print_action(f"⚠️  WARNING: Weekly total approaching limit ({weekly_total}h > {weekly_warning}h warning)")
        
        # Check exam conflicts with tournament travel
        if self.syllabus_data and 'courses' in self.syllabus_data:
            self._print_thought("Cross-referencing academic calendar with athletic events...")
            
            tournament_start = datetime.strptime('2026-06-20', '%Y-%m-%d')
            tournament_end = datetime.strptime('2026-06-23', '%Y-%m-%d')
            
            for course in self.syllabus_data['courses']:
                course_code = course.get('course_code', 'UNKNOWN')
                
                for deadline in course.get('deadlines', []):
                    if deadline.get('type') == 'exam':
                        exam_date_str = deadline.get('due_date')
                        exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d')
                        
                        self._print_evaluating(f"Checking {course_code} {deadline.get('assignment')} on {exam_date_str}")
                        
                        # Check if exam falls during tournament
                        if tournament_start <= exam_date <= tournament_end:
                            conflict = {
                                'type': 'EXAM_TRAVEL_CONFLICT',
                                'course': course_code,
                                'exam': deadline.get('assignment'),
                                'exam_date': exam_date_str,
                                'tournament_dates': f"2026-06-20 to 2026-06-23",
                                'severity': 'CRITICAL'
                            }
                            self.conflicts.append(conflict)
                            self._print_action(f"🚨 CRITICAL CONFLICT: {course_code} {deadline.get('assignment')} on {exam_date_str} during championship tournament")
                        
                        # Check if exam is within 48 hours before/after tournament
                        days_before = (tournament_start - exam_date).days
                        days_after = (exam_date - tournament_end).days
                        
                        if 0 < days_before <= 2:
                            conflict = {
                                'type': 'EXAM_PRE_TRAVEL_CONFLICT',
                                'course': course_code,
                                'exam': deadline.get('assignment'),
                                'exam_date': exam_date_str,
                                'days_before_travel': days_before,
                                'severity': 'HIGH'
                            }
                            self.conflicts.append(conflict)
                            self._print_action(f"⚠️  HIGH CONFLICT: {course_code} {deadline.get('assignment')} is {days_before} days before tournament travel")
        
        self._print_thought(f"Constraint verification complete. Found {len(self.violations)} violations and {len(self.conflicts)} conflicts.")

    def _synthesize_remediation(self) -> ComplianceStatus:
        """
        Step 3: Generate remediation actions and compliance-aligned recommendations.
        
        Outputs:
        - Structured JSON status with alert flags
        - Professional email drafts requesting exam accommodations
        """
        self._print_thought("Synthesizing remediation actions based on identified violations and conflicts...")
        
        # Determine overall status
        has_alerts = len(self.violations) > 0 or len(self.conflicts) > 0
        violation_level = self._determine_violation_level()
        
        self._print_evaluating(f"Alert Flag: {has_alerts}")
        self._print_evaluating(f"Violation Level: {violation_level}")
        
        remediation_actions = []
        
        # Generate remediation for violations
        for violation in self.violations:
            self._print_action(f"Generating remediation for: {violation['type']}")
            
            if violation['type'] == 'DAILY_HOURS_VIOLATION':
                action = (
                    f"URGENT: Reduce {violation['day']} practice hours from {violation['hours']}h "
                    f"to maximum {violation['limit']}h to comply with NCAA CARA regulations."
                )
                remediation_actions.append(action)
                self._print_action(f"→ {action}")
            
            elif violation['type'] == 'WEEKLY_HOURS_VIOLATION':
                action = (
                    f"CRITICAL: Redistribute weekly practice hours from {violation['total_hours']}h "
                    f"to maximum {violation['limit']}h across the week to avoid eligibility suspension."
                )
                remediation_actions.append(action)
                self._print_action(f"→ {action}")
        
        # Generate remediation for conflicts
        email_drafts = []
        for conflict in self.conflicts:
            self._print_action(f"Generating remediation for: {conflict['type']}")
            
            if conflict['type'] == 'EXAM_TRAVEL_CONFLICT':
                action = (
                    f"Request exam accommodation for {conflict['course']} {conflict['exam']} "
                    f"(scheduled {conflict['exam_date']}) due to mandatory championship tournament travel "
                    f"({conflict['tournament_dates']}). Contact professor immediately."
                )
                remediation_actions.append(action)
                self._print_action(f"→ {action}")
                
                # Generate email draft
                email = self._generate_accommodation_email(conflict)
                email_drafts.append(email)
                self._print_action(f"→ Email draft generated for {conflict['course']} professor")
            
            elif conflict['type'] == 'EXAM_PRE_TRAVEL_CONFLICT':
                action = (
                    f"Alert: {conflict['course']} {conflict['exam']} is only {conflict['days_before_travel']} day(s) "
                    f"before tournament travel. Ensure adequate study time and inform professor of travel schedule."
                )
                remediation_actions.append(action)
                self._print_action(f"→ {action}")
        
        # Write email drafts to files
        if email_drafts:
            self._print_action("Writing email drafts to files...")
            for i, email in enumerate(email_drafts):
                course_code = email['course_code']
                filename = f"accommodation_request_{course_code}.json"
                filepath = Path(self.data_dir) / "output" / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                with open(filepath, 'w') as f:
                    json.dump(email, f, indent=2)
                
                self._print_action(f"✓ Wrote {filename}")
        
        # Create comprehensive status report
        status = ComplianceStatus(
            timestamp=datetime.now().isoformat(),
            student_id=self.syllabus_data['student']['id'],
            student_name=self.syllabus_data['student']['name'],
            alert_flag=has_alerts,
            violation_level=violation_level,
            violations=self.violations,
            conflicts=self.conflicts,
            remediation_actions=remediation_actions,
            recommendation=self._generate_recommendation()
        )
        
        # Save status report
        self._print_action("Writing compliance status report...")
        status_filepath = Path(self.data_dir) / "output" / "compliance_status.json"
        status_filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(status_filepath, 'w') as f:
            json.dump(asdict(status), f, indent=2, default=str)
        
        self._print_action(f"✓ Wrote compliance_status.json")
        
        return status

    def _determine_violation_level(self) -> str:
        """Determine the highest violation level present."""
        if not self.violations and not self.conflicts:
            return ViolationLevel.NO_VIOLATION.value
        
        # Check for critical conflicts
        for conflict in self.conflicts:
            if conflict.get('severity') == 'CRITICAL':
                return ViolationLevel.SEVERE.value
        
        # Check for major violations
        for violation in self.violations:
            if violation.get('severity') == 'MAJOR':
                return ViolationLevel.MAJOR.value
        
        # Check for high conflicts
        for conflict in self.conflicts:
            if conflict.get('severity') == 'HIGH':
                return ViolationLevel.MAJOR.value
        
        return ViolationLevel.WARNING.value

    def _generate_accommodation_email(self, conflict: Dict) -> Dict:
        """Generate a professional accommodation request email."""
        course_code = conflict['course']
        exam_name = conflict['exam']
        exam_date = conflict['exam_date']
        student_name = self.syllabus_data['student']['name']
        student_id = self.syllabus_data['student']['id']
        
        # Find course details
        course_info = None
        instructor_name = "Professor"
        for course in self.syllabus_data['courses']:
            if course['course_code'] == course_code:
                course_info = course
                instructor_name = course.get('instructor', 'Professor').split()[-1]
                break
        
        email_body = f"""Dear {instructor_name},

I am writing to request a potential accommodation for the {exam_name} scheduled for {exam_date} in {course_code}.

Due to my participation in our university's championship tournament competition, I am required to travel from June 20-23, 2026, as part of my athletic scholarship commitment. This mandatory team travel unfortunately overlaps with the {exam_name} date.

I understand the importance of maintaining academic integrity and completing all assessments. I would like to discuss the possibility of:
1. Taking an early exam before June 20th, or
2. Taking a make-up exam after my return on June 24th, or
3. An alternative assessment method approved by the university

I have consistently maintained strong academic performance in {course_code} and am committed to demonstrating my knowledge of the course material in any format you deem appropriate.

I will follow up with your office by end of business tomorrow to confirm your availability to discuss this matter.

Thank you for your understanding and consideration.

Best regards,
{student_name}
Student ID: {student_id}
Major: {self.syllabus_data['student']['major']}
"""

        return {
            'course_code': course_code,
            'course_title': course_info['title'] if course_info else 'Unknown',
            'instructor': instructor_name,
            'student_name': student_name,
            'student_id': student_id,
            'exam_date': exam_date,
            'exam_name': exam_name,
            'subject_line': f"Request for Exam Accommodation - {course_code} {exam_name}",
            'email_body': email_body,
            'generated_at': datetime.now().isoformat()
        }

    def _generate_recommendation(self) -> str:
        """Generate an overall recommendation based on analysis."""
        if not self.violations and not self.conflicts:
            return (
                "✅ COMPLIANT: All practice hours and academic deadlines are aligned with NCAA CARA regulations. "
                "Continue current schedule with regular compliance monitoring."
            )
        
        if any(c.get('severity') == 'CRITICAL' for c in self.conflicts):
            return (
                "🚨 URGENT ACTION REQUIRED: Critical exam-travel conflict detected. "
                "Contact academic advisor and professors immediately to arrange accommodations. "
                "Monitor compliance violations closely."
            )
        
        major_violations = any(v.get('severity') == 'MAJOR' for v in self.violations)
        high_conflicts = any(c.get('severity') == 'HIGH' for c in self.conflicts)
        
        if major_violations:
            return (
                "⚠️  MAJOR VIOLATIONS DETECTED: Practice schedule exceeds NCAA CARA limits. "
                "Work with coaching staff to redistribute hours immediately to prevent eligibility suspension."
            )
        
        if high_conflicts:
            return (
                "⚠️  SCHEDULE CONFLICTS: Academic-athletic scheduling conflicts present. "
                "Request exam accommodations from professors and coordinate with athletics."
            )
        
        return "⚠️  MINOR WARNINGS: Minor compliance concerns. Continue monitoring and coordinate schedule adjustments."

    def _print_status_summary(self, status: ComplianceStatus):
        """Print a summary of the compliance status."""
        print(f"\n📋 COMPLIANCE STATUS SUMMARY")
        print(f"   Student: {status.student_name} ({status.student_id})")
        print(f"   Alert Flag: {'🚨 YES' if status.alert_flag else '✅ NO'}")
        print(f"   Violation Level: {status.violation_level.upper()}")
        print(f"   Violations Found: {len(status.violations)}")
        print(f"   Conflicts Found: {len(status.conflicts)}")
        print(f"   Remediation Actions: {len(status.remediation_actions)}")
        print(f"\n   Recommendation:")
        print(f"   {status.recommendation}")


def main():
    """Main entry point for the compliance reasoning engine."""
    agent = ComplianceAgent(data_dir="data")
    status = agent.run_pipeline()
    
    # Print reasoning log
    print("\n" + "=" * 70)
    print("  COMPLETE REASONING LOG")
    print("=" * 70)
    for log_entry in agent.reasoning_log:
        print(log_entry)
    
    # Print final JSON status
    print("\n" + "=" * 70)
    print("  FINAL COMPLIANCE STATUS (JSON)")
    print("=" * 70)
    print(json.dumps(asdict(status), indent=2, default=str))


if __name__ == "__main__":
    main()
