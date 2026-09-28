"""A command-line student management system."""

from __future__ import annotations


class Person:
    def __init__(self, name: str, age: int, person_id: str) -> None:
        self.name = name
        self.age = age
        self.person_id = person_id

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, age={self.age}, id={self.person_id!r})"


class Student(Person):
    def __init__(self, name: str, age: int, student_id: str, grade_level: str) -> None:
        super().__init__(name, age, student_id)
        self.grade_level = grade_level
        self.enrolled_courses: list[Course] = []

    def __repr__(self) -> str:
        return (f"Student(name={self.name!r}, age={self.age}, id={self.person_id!r}, "
                f"grade_level={self.grade_level!r})")

    def enroll_in_course(self, course: Course) -> None:
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)

    def drop_course(self, course: Course) -> None:
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)


class Course:
    def __init__(self, course_name: str, course_id: str, instructor: str) -> None:
        self.course_name = course_name
        self.course_id = course_id
        self.instructor = instructor
        self.students: list[Student] = []

    def __repr__(self) -> str:
        return (f"Course(name={self.course_name!r}, id={self.course_id!r}, "
                f"instructor={self.instructor!r})")

    def add_student(self, student: Student) -> None:
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student: Student) -> None:
        if student in self.students:
            self.students.remove(student)


class StudentManagementSystem:
    """Keeps students and courses by ID. Every method prints what happened and
    returns True on success, False otherwise."""

    def __init__(self) -> None:
        self.students: dict[str, Student] = {}
        self.courses: dict[str, Course] = {}

    def add_student(self, name: str, age: int, student_id: str, grade_level: str) -> bool:
        if not name or not student_id:
            print("Name and student ID cannot be empty.")
            return False
        if age <= 0:
            print("Age must be a positive number.")
            return False
        if student_id in self.students:
            print("Student ID already exists.")
            return False
        self.students[student_id] = Student(name, age, student_id, grade_level)
        print(f"Student {name} added.")
        return True

    def remove_student(self, student_id: str) -> bool:
        student = self.students.pop(student_id, None)
        if student is None:
            print("Student ID not found.")
            return False
        # take the student off every course roster as well
        for course in student.enrolled_courses:
            course.remove_student(student)
        print("Student removed.")
        return True

    def add_course(self, course_name: str, course_id: str, instructor: str) -> bool:
        if not course_name or not course_id:
            print("Course name and course ID cannot be empty.")
            return False
        if course_id in self.courses:
            print("Course ID already exists.")
            return False
        self.courses[course_id] = Course(course_name, course_id, instructor)
        print(f"Course {course_name} added.")
        return True

    def remove_course(self, course_id: str) -> bool:
        course = self.courses.pop(course_id, None)
        if course is None:
            print("Course ID not found.")
            return False
        # remove the course from the schedule of every enrolled student
        for student in course.students:
            student.drop_course(course)
        print("Course removed.")
        return True

    def enroll_student(self, student_id: str, course_id: str) -> bool:
        student = self.students.get(student_id)
        course = self.courses.get(course_id)
        if not student or not course:
            print("Invalid student or course ID.")
            return False
        if course in student.enrolled_courses:
            print(f"{student.name} is already enrolled in {course.course_name}.")
            return False
        student.enroll_in_course(course)
        course.add_student(student)
        print(f"Student {student.name} enrolled in {course.course_name}.")
        return True

    def drop_student(self, student_id: str, course_id: str) -> bool:
        student = self.students.get(student_id)
        course = self.courses.get(course_id)
        if not student or not course:
            print("Invalid student or course ID.")
            return False
        if course not in student.enrolled_courses:
            print(f"{student.name} is not enrolled in {course.course_name}.")
            return False
        student.drop_course(course)
        course.remove_student(student)
        print(f"Student {student.name} dropped {course.course_name}.")
        return True

    def view_student_courses(self, student_id: str) -> None:
        student = self.students.get(student_id)
        if not student:
            print("Student ID not found.")
            return
        if not student.enrolled_courses:
            print(f"{student.name} is not enrolled in any courses.")
            return
        print(f"{student.name}'s courses:")
        for course in student.enrolled_courses:
            print(f"- {course.course_name} (ID: {course.course_id})")

    def view_course_students(self, course_id: str) -> None:
        course = self.courses.get(course_id)
        if not course:
            print("Course ID not found.")
            return
        if not course.students:
            print(f"No students enrolled in {course.course_name}.")
            return
        print(f"Students in {course.course_name}:")
        for student in course.students:
            print(f"- {student.name} (ID: {student.person_id})")

    def list_students(self) -> None:
        if not self.students:
            print("No students registered.")
            return
        print("Registered students:")
        for sid, student in self.students.items():
            print(f"- {student.name} (ID: {sid}, age: {student.age}, grade: {student.grade_level})")

    def list_courses(self) -> None:
        if not self.courses:
            print("No courses available.")
            return
        print("Available courses:")
        for cid, course in self.courses.items():
            print(f"- {course.course_name} (ID: {cid}, instructor: {course.instructor}, "
                  f"students: {len(course.students)})")


def ask(prompt: str) -> str:
    return input(prompt).strip()


def ask_positive_int(prompt: str) -> int:
    while True:
        text = ask(prompt)
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Please enter a positive whole number.")


MENU = """
Student Management System
1. Add Student
2. Remove Student
3. Add Course
4. Remove Course
5. Enroll Student in Course
6. Drop Student from Course
7. View Student's Courses
8. View Course Roster
9. List All Students
10. List All Courses
0. Exit"""


def run_menu(system: StudentManagementSystem) -> None:
    while True:
        print(MENU)
        choice = ask("Enter your choice: ")

        if choice == "1":
            name = ask("Enter student name: ")
            age = ask_positive_int("Enter student age: ")
            student_id = ask("Enter student ID: ")
            grade_level = ask("Enter grade level: ")
            system.add_student(name, age, student_id, grade_level)
        elif choice == "2":
            system.remove_student(ask("Enter student ID to remove: "))
        elif choice == "3":
            course_name = ask("Enter course name: ")
            course_id = ask("Enter course ID: ")
            instructor = ask("Enter instructor name: ")
            system.add_course(course_name, course_id, instructor)
        elif choice == "4":
            system.remove_course(ask("Enter course ID to remove: "))
        elif choice == "5":
            student_id = ask("Enter student ID: ")
            course_id = ask("Enter course ID: ")
            system.enroll_student(student_id, course_id)
        elif choice == "6":
            student_id = ask("Enter student ID: ")
            course_id = ask("Enter course ID: ")
            system.drop_student(student_id, course_id)
        elif choice == "7":
            system.view_student_courses(ask("Enter student ID: "))
        elif choice == "8":
            system.view_course_students(ask("Enter course ID: "))
        elif choice == "9":
            system.list_students()
        elif choice == "10":
            system.list_courses()
        elif choice == "0":
            print("Exiting system...")
            return
        else:
            print("Invalid choice. Please try again.")


def main() -> None:
    try:
        run_menu(StudentManagementSystem())
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D / Ctrl+Z or Ctrl+C: leave quietly instead of a traceback
        print("\nExiting system...")


if __name__ == "__main__":
    main()
