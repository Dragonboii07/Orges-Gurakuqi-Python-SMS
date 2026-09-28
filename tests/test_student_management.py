import contextlib
import io
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from student_management import StudentManagementSystem, main  # noqa: E402


class StudentManagementSystemTest(unittest.TestCase):
    def setUp(self):
        self.system = StudentManagementSystem()
        # keep the test output clean
        self._quiet = contextlib.redirect_stdout(io.StringIO())
        self._quiet.__enter__()
        self.system.add_student("Anna", 20, "S1", "10")
        self.system.add_student("Ben", 21, "S2", "11")
        self.system.add_course("Math", "C1", "Dr. Smith")

    def tearDown(self):
        self._quiet.__exit__(None, None, None)

    def test_rejects_duplicate_and_invalid_students(self):
        self.assertFalse(self.system.add_student("Other", 30, "S1", "12"))
        self.assertFalse(self.system.add_student("", 30, "S3", "12"))
        self.assertFalse(self.system.add_student("Zed", 0, "S3", "12"))
        self.assertEqual(len(self.system.students), 2)

    def test_enroll_links_both_sides(self):
        self.assertTrue(self.system.enroll_student("S1", "C1"))
        self.assertFalse(self.system.enroll_student("S1", "C1"))
        self.assertEqual([c.course_id for c in self.system.students["S1"].enrolled_courses], ["C1"])
        self.assertEqual([s.person_id for s in self.system.courses["C1"].students], ["S1"])

    def test_enroll_with_unknown_ids(self):
        self.assertFalse(self.system.enroll_student("S9", "C1"))
        self.assertFalse(self.system.enroll_student("S1", "C9"))

    def test_drop_student(self):
        self.system.enroll_student("S1", "C1")
        self.assertTrue(self.system.drop_student("S1", "C1"))
        self.assertFalse(self.system.drop_student("S1", "C1"))
        self.assertEqual(self.system.courses["C1"].students, [])
        self.assertEqual(self.system.students["S1"].enrolled_courses, [])

    def test_removing_student_clears_rosters(self):
        self.system.enroll_student("S1", "C1")
        self.system.enroll_student("S2", "C1")
        self.assertTrue(self.system.remove_student("S1"))
        self.assertEqual([s.person_id for s in self.system.courses["C1"].students], ["S2"])

    def test_removing_course_clears_schedules(self):
        self.system.enroll_student("S1", "C1")
        self.assertTrue(self.system.remove_course("C1"))
        self.assertEqual(self.system.students["S1"].enrolled_courses, [])
        self.assertFalse(self.system.remove_course("C1"))


class MenuTest(unittest.TestCase):
    def run_menu(self, *answers):
        out = io.StringIO()
        with mock.patch("builtins.input", side_effect=list(answers)), contextlib.redirect_stdout(out):
            main()
        return out.getvalue()

    def test_full_session(self):
        output = self.run_menu(
            "1", "Anna", "abc", "20", "S1", "10",  # bad age is asked again
            "3", "Math", "C1", "Dr. Smith",
            "5", "S1", "C1",
            "8", "C1",
            "0",
        )
        self.assertIn("Please enter a positive whole number.", output)
        self.assertIn("Student Anna enrolled in Math.", output)
        self.assertIn("- Anna (ID: S1)", output)
        self.assertIn("Exiting system...", output)

    def test_end_of_input_exits_cleanly(self):
        output = self.run_menu("9", EOFError())  # like pressing Ctrl+D at the prompt
        self.assertIn("No students registered.", output)
        self.assertIn("Exiting system...", output)


if __name__ == "__main__":
    unittest.main()
