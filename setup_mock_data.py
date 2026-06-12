#!/usr/bin/env python3
"""
ScoutFlow AI - Mock Data Setup Script
Creates realistic mock data files for Work IQ layer simulation without M365 connection.

This script generates:
- messy_schedule.txt: Unstructured coach email with schedule changes
- syllabus_deadlines.json: Academic calendar and course deadlines
- compliance_rules.json: NCAA CARA regulation thresholds
"""

import os
import json
from pathlib import Path

# Define the data directory
DATA_DIR = Path(__file__).parent / "data"


def create_data_directory():
    """Create /data directory if it doesn't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    print(f"✓ Data directory ready: {DATA_DIR}")


def create_messy_schedule():
    """Create mock chaotic email from coach about schedule changes."""
    messy_schedule_content = """FROM: Coach Martinez <coach.martinez@university.edu>
TO: Sarah Chen <sarah.chen@university.edu>
DATE: June 10, 2026
SUBJECT: URGENT - Schedule Change + Flight Update

Hey Sarah,

quick heads up on some last-minute changes - just got word from athletics director this afternoon.

1) Your flight to Dallas for the championship tournament - the 2:45 PM departure on June 20th is CANCELLED. We've moved you to the 6:30 AM flight SAME DAY (still June 20). Yeah I know that's early but we need to get there for team check-in by 10 AM. New confirmation number is DELTA-7849KL. Gate info will be sent tomorrow.

2) Practice schedule shift - Since we lost two days to the tournament, we're extending practice hours starting Monday June 15th:
   - Monday through Thursday: 3 hours/day (normally 2.5)
   - Friday: 4 hours (strength & conditioning focus)
   
This is on top of your regular conditioning sessions, which remain at 1.5 hours on MWF.

3) Also, make sure you've completed your NCAA compliance forms by end of business Friday or you won't be cleared to compete.

Let me know if you have any conflicts with the new flight. The athletic trainer will be at the airport with the team.

-Coach M

P.S. - Don't forget about the film review Wednesday 7-9 PM with the team. That's NOT counted in the practice hours above but required attendance.
"""
    
    filepath = DATA_DIR / "messy_schedule.txt"
    with open(filepath, "w") as f:
        f.write(messy_schedule_content)
    print(f"✓ Created: {filepath}")


def create_syllabus_deadlines():
    """Create mock academic calendar and course deadlines."""
    syllabus_deadlines = {
        "student": {
            "id": "SC-2024-08421",
            "name": "Sarah Chen",
            "major": "Business Analytics",
            "graduation_year": 2027
        },
        "academic_calendar": {
            "current_semester": "Summer 2026",
            "semester_start": "2026-06-01",
            "semester_end": "2026-08-15"
        },
        "courses": [
            {
                "course_code": "BUS-301",
                "title": "Financial Analysis",
                "instructor": "Dr. Patricia Wong",
                "credits": 3,
                "meeting_times": "MWF 10:00-11:00 AM",
                "deadlines": [
                    {
                        "assignment": "Case Study 1",
                        "due_date": "2026-06-15",
                        "type": "individual",
                        "weight": 0.15
                    },
                    {
                        "assignment": "Midterm Exam",
                        "due_date": "2026-06-22",
                        "type": "exam",
                        "weight": 0.30,
                        "notes": "Covers chapters 1-8, 2 hours, in-person at Classroom 204"
                    },
                    {
                        "assignment": "Group Project - Proposal",
                        "due_date": "2026-06-29",
                        "type": "group",
                        "weight": 0.20,
                        "notes": "4-person team, 10-page proposal minimum"
                    },
                    {
                        "assignment": "Final Exam",
                        "due_date": "2026-08-10",
                        "type": "exam",
                        "weight": 0.35,
                        "notes": "Cumulative, 3 hours, comprehensive"
                    }
                ]
            },
            {
                "course_code": "MATH-215",
                "title": "Statistics for Business",
                "instructor": "Dr. James Liu",
                "credits": 3,
                "meeting_times": "TTh 2:00-3:30 PM",
                "deadlines": [
                    {
                        "assignment": "Problem Set 3",
                        "due_date": "2026-06-17",
                        "type": "homework",
                        "weight": 0.10
                    },
                    {
                        "assignment": "Quiz 2",
                        "due_date": "2026-06-24",
                        "type": "quiz",
                        "weight": 0.25,
                        "notes": "Online, 45 minutes, multiple choice and short answer"
                    },
                    {
                        "assignment": "Data Analysis Project",
                        "due_date": "2026-07-15",
                        "type": "project",
                        "weight": 0.35
                    },
                    {
                        "assignment": "Final Exam",
                        "due_date": "2026-08-12",
                        "type": "exam",
                        "weight": 0.30
                    }
                ]
            }
        ],
        "athletic_calendar": [
            {
                "event": "Conference Championship Tournament - Dallas",
                "start_date": "2026-06-20",
                "end_date": "2026-06-23",
                "travel_required": True,
                "notes": "Early flight 6:30 AM June 20, confirmation DELTA-7849KL"
            },
            {
                "event": "Post-Season Training Camp",
                "start_date": "2026-07-08",
                "end_date": "2026-07-14",
                "travel_required": False,
                "intensity": "high"
            }
        ],
        "important_notes": "Sarah is a student-athlete balancing intense academic coursework with competitive athletics. June 22 midterm exam conflicts with championship tournament travel. Recommend early exam accommodation request or alternative assessment method."
    }
    
    filepath = DATA_DIR / "syllabus_deadlines.json"
    with open(filepath, "w") as f:
        json.dump(syllabus_deadlines, f, indent=2)
    print(f"✓ Created: {filepath}")


def create_compliance_rules():
    """Create mock NCAA CARA regulation thresholds."""
    compliance_rules = {
        "compliance_framework": "NCAA CARA (Collegiate Athlete Responsibilities and Accountability)",
        "effective_date": "2026-01-01",
        "sport": "All",
        "regulation_version": "2026-2027",
        "rules": {
            "practice_hours": {
                "daily_maximum_hours": 4,
                "daily_maximum_minutes": 240,
                "description": "Maximum allowable practice/training per calendar day",
                "enforcement": "Strict",
                "violation_consequence": "Potential eligibility suspension"
            },
            "weekly_hours": {
                "weekly_maximum_hours": 20,
                "weekly_maximum_minutes": 1200,
                "description": "Maximum allowable practice/training per academic week (Sunday-Saturday)",
                "enforcement": "Strict",
                "violation_consequence": "Potential eligibility suspension"
            },
            "training_sessions": {
                "maximum_per_day": 2,
                "minimum_rest_between_sessions_hours": 4,
                "description": "No more than 2 organized practice sessions per day with minimum 4-hour rest",
                "enforcement": "Moderate",
                "violation_consequence": "Program warning, possible reduced hours"
            },
            "mandatory_rest": {
                "rest_days_per_week": 1,
                "consecutive_days_off_per_month": 4,
                "description": "At least 1 complete rest day per week; minimum 4 consecutive days off per calendar month",
                "enforcement": "Strict",
                "violation_consequence": "Potential eligibility suspension"
            },
            "off_season_restrictions": {
                "strength_conditioning_max_hours_per_week": 8,
                "practice_prohibited": True,
                "description": "Off-season (outside competition dates) limited to strength/conditioning only",
                "enforcement": "Moderate",
                "note": "Definitions of on-season vs off-season vary by sport"
            },
            "counting_rules": {
                "what_counts_as_practice": [
                    "Team meetings related to sport",
                    "Strength and conditioning sessions",
                    "Practice drills and scrimmages",
                    "Mandatory film review",
                    "Organized position coaching",
                    "Team travel for competition"
                ],
                "what_does_not_count": [
                    "Voluntary individual training (gym workouts without coach)",
                    "Equipment maintenance/setup",
                    "Meals/dining",
                    "Casual workouts not organized by coaching staff"
                ],
                "gray_areas": [
                    "Film review (counts if mandatory, not if voluntary)",
                    "Team meals (counts only if structured activity time)",
                    "Media obligations (typically does not count)"
                ]
            },
            "exceptions": {
                "championship_tournament_week": {
                    "daily_maximum_hours": 6,
                    "weekly_cap_applies": False,
                    "duration": "Maximum 7 consecutive days per calendar year",
                    "notes": "NCAA allows temporary increase during official championship tournament weeks"
                },
                "emergency_situations": {
                    "approved_by": "Athletics Director + Compliance Officer",
                    "maximum_extension_hours": 2,
                    "maximum_days_per_year": 3,
                    "notes": "Rare exceptions for unforeseen circumstances"
                }
            },
            "monitoring_requirements": {
                "tracking_method": "Coach must log all practice hours daily",
                "report_frequency": "Weekly submission to compliance office",
                "audit_frequency": "Monthly random audits",
                "documentation": "Coach signature required on all logs"
            },
            "penalties": {
                "first_violation": {
                    "level": "Minor",
                    "consequence": "Program warning, mandatory education"
                },
                "second_violation": {
                    "level": "Major",
                    "consequence": "Reduced allowed hours for 30 days, possible partial eligibility suspension"
                },
                "third_violation": {
                    "level": "Severe",
                    "consequence": "Full eligibility suspension until compliance certification completed"
                }
            }
        },
        "work_iq_thresholds": {
            "daily_hours_warning_threshold": 3.5,
            "weekly_hours_warning_threshold": 18,
            "note": "ScoutFlow AI should flag alerts when approaching 87.5% of daily and 90% of weekly limits"
        },
        "school_specific_rules": {
            "institution": "State University",
            "additional_restrictions": [
                "No practice sessions before 7:00 AM",
                "No practice sessions after 9:00 PM",
                "Mandatory 12-hour break between practice sessions",
                "All practices must be scheduled 48 hours in advance with compliance office"
            ],
            "approval_authority": "Director of Athletics, Compliance Officer: compliance@stateuniversity.edu"
        }
    }
    
    filepath = DATA_DIR / "compliance_rules.json"
    with open(filepath, "w") as f:
        json.dump(compliance_rules, f, indent=2)
    print(f"✓ Created: {filepath}")


def main():
    """Main function to set up all mock data."""
    print("=" * 60)
    print("ScoutFlow AI - Mock Data Setup")
    print("=" * 60)
    
    try:
        create_data_directory()
        create_messy_schedule()
        create_syllabus_deadlines()
        create_compliance_rules()
        
        print("\n" + "=" * 60)
        print("✅ All mock data files created successfully!")
        print("=" * 60)
        print(f"\nData files location: {DATA_DIR}")
        print("\nFiles created:")
        print(f"  1. {DATA_DIR / 'messy_schedule.txt'}")
        print(f"  2. {DATA_DIR / 'syllabus_deadlines.json'}")
        print(f"  3. {DATA_DIR / 'compliance_rules.json'}")
        print("\nYou can now use these mock files to simulate the Work IQ layer")
        print("without connecting to a production M365 tenant.")
        
    except Exception as e:
        print(f"\n❌ Error creating mock data: {e}")
        raise


if __name__ == "__main__":
    main()
