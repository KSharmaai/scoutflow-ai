import sys
import unittest
from pathlib import Path

# Ensure src is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agents.compliance import ComplianceAgent


class TestComplianceAgent(unittest.TestCase):
    def test_honorific_parsing_dr(self):
        """Raw 'Dr. Patricia Wong' should map to 'Dr. Wong' and email starts with Dear Dr. Wong,"""
        agent = ComplianceAgent(data_dir="data")

        conflict = {
            'course': 'BUS-301',
            'exam': 'Midterm Exam',
            'exam_date': '2026-06-22',
            'tournament_dates': '2026-06-20 to 2026-06-23'
        }

        email = agent._generate_accommodation_email(conflict)

        # Instructor greeting should use honorific + last name
        self.assertIn('instructor', email)
        self.assertEqual(email['instructor'], 'Dr. Wong')
        self.assertTrue(email['email_body'].strip().startswith('Dear Dr. Wong,'))

    def test_honorific_parsing_professor(self):
        """Handles 'Professor James Liu' entries, mapping to 'Professor Liu' greeting."""
        agent = ComplianceAgent(data_dir="data")

        # Inject a syllabus override so we can test a Professor honorific
        agent.syllabus_data = {
            'student': {
                'id': 'TEST-001',
                'name': 'Test Student',
                'major': 'Testing'
            },
            'courses': [
                {
                    'course_code': 'MATH-215',
                    'title': 'Statistics for Business',
                    'instructor': 'Professor James Liu',
                    'deadlines': [
                        {'assignment': 'Final Exam', 'due_date': '2026-08-12', 'type': 'exam'}
                    ]
                }
            ]
        }

        conflict = {
            'course': 'MATH-215',
            'exam': 'Final Exam',
            'exam_date': '2026-08-12',
            'tournament_dates': '2026-08-10 to 2026-08-14'
        }

        email = agent._generate_accommodation_email(conflict)
        self.assertEqual(email['instructor'], 'Professor Liu')
        self.assertTrue(email['email_body'].strip().startswith('Dear Professor Liu,'))

    def test_cara_hours_weekly_aggregation(self):
        """Validate weekly aggregation equals 19.0 and triggers a warning over 18h threshold."""
        agent = ComplianceAgent(data_dir="data")

        # Run parsing and verification steps
        agent._parse_schedule()
        agent._verify_constraints()

        # Check reasoning log contains the weekly total calculation and warning
        joined = "\n".join(agent.reasoning_log)
        self.assertIn('Weekly Total Calculated', joined)
        # Expect 19.0 total
        self.assertIn('19.0', joined)
        # Expect a warning about approaching weekly threshold (18h)
        self.assertIn('approaching limit', joined.lower())


if __name__ == '__main__':
    unittest.main()
