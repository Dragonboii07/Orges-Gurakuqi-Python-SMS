# Student Management System (Python)

A command-line student management system written in Python. You can add and
remove students and courses, enroll students in courses, drop them again and
view rosters, all from a numbered menu.

## Features

* `Person`, `Student` and `Course` classes, with `Student` inheriting from `Person`
* `StudentManagementSystem` that keeps students and courses by ID
* Enrollments are kept in sync on both sides: removing a student takes them
  off every roster, and removing a course takes it off every schedule
* Input validation: no empty names or IDs, no duplicate IDs, age must be a
  positive number (you are asked again instead of being sent back to the menu)
* Exits cleanly on Ctrl+C or end of input instead of crashing
* Unit tests using Python's built-in `unittest`, no extra packages needed

## Requirements

Python 3.9 or newer. There are no third-party dependencies.

## Running

```bash
git clone https://github.com/Dragonboii07/Orges-Gurakuqi-Python-SMS.git
cd Orges-Gurakuqi-Python-SMS
python student_management.py
```

On some systems the command is `python3` instead of `python`.

## Menu

| Choice | Action                    |
|--------|---------------------------|
| 1      | Add student               |
| 2      | Remove student            |
| 3      | Add course                |
| 4      | Remove course             |
| 5      | Enroll student in course  |
| 6      | Drop student from course  |
| 7      | View a student's courses  |
| 8      | View a course roster      |
| 9      | List all students         |
| 10     | List all courses          |
| 0      | Exit                      |

Example session:

```text
Enter your choice: 1
Enter student name: Anna
Enter student age: 20
Enter student ID: S1
Enter grade level: 10
Student Anna added.
...
Enter your choice: 5
Enter student ID: S1
Enter course ID: C1
Student Anna enrolled in Math.
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Credits

Designed and built by Orges Gurakuqi: the class design, the management
system and the menu-driven interface.

I used an AI coding assistant (Claude) to review and polish the code. It
helped me fix enrollments being left behind when a student or course was
removed, add the drop-course option and input validation, clean up the README
and write the unit tests.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for
details.
