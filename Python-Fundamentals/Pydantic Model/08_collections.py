# ============================================================
#    PYDANTIC - LIST, SET, DICTIONARY & NESTED COLLECTIONS
# ============================================================

from pydantic import BaseModel


# Subject Model

class Subject(BaseModel):
    name: str
    marks: int


# Student Model

class Student(BaseModel):
    name: str
    age: int

    # List of strings
    skills: list[str]

    # List of integers
    scores: list[int]

    # Set of strings
    languages: set[str]

    # Dictionary
    subject_marks: dict[str, int]

    # List of Pydantic Models
    subjects: list[Subject]


# Create Student

student = Student(
    name="Gaurav",
    age=22,

    # list[str]
    skills=[
        "Python",
        "FastAPI",
        "Pydantic"
    ],

    # list[int]
    scores=[
        90,
        85,
        95
    ],

    # set[str]
    languages={
        "Hindi",
        "English"
    },

    # dict[str, int]
    subject_marks={
        "Python": 95,
        "SQL": 90
    },

    # list[Subject]
    subjects=[
        Subject(
            name="Python",
            marks=95
        ),
        Subject(
            name="SQL",
            marks=90
        )
    ]
)


# Print Complete Student

print("Student:")
print(student)


# List of Strings
# ------------------------------------------------------------

print("\nSkills:")
print(student.skills)


# List of Integers
# ------------------------------------------------------------

print("\nScores:")
print(student.scores)


# Set of Strings
# ------------------------------------------------------------

print("\nLanguages:")
print(student.languages)


# Dictionary
# ------------------------------------------------------------

print("\nSubject Marks:")
print(student.subject_marks)


# List of Pydantic Models
# ------------------------------------------------------------

print("\nSubjects:")

for subject in student.subjects:
    print(subject)


# Access Nested Collection
# ------------------------------------------------------------

print("\nFirst Subject Name:")
print(student.subjects[0].name)

print("\nFirst Subject Marks:")
print(student.subjects[0].marks)