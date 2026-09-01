# ============================================================
#    PYDANTIC - LIST, SET, DICTIONARY & NESTED COLLECTIONS
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


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

@app.post("/students")
def create_student(student: Student):


    # Print Complete Student

    print("Student:")
    print(student)


    # List of Strings
    # --------------------------------------------------------

    print("\nSkills:")
    print(student.skills)


    # List of Integers
    # --------------------------------------------------------

    print("\nScores:")
    print(student.scores)


    # Set of Strings
    # --------------------------------------------------------

    print("\nLanguages:")
    print(student.languages)


    # Dictionary
    # --------------------------------------------------------

    print("\nSubject Marks:")
    print(student.subject_marks)


    # List of Pydantic Models
    # --------------------------------------------------------

    print("\nSubjects:")

    for subject in student.subjects:
        print(subject)


    # Access Nested Collection
    # --------------------------------------------------------

    print("\nFirst Subject Name:")
    print(student.subjects[0].name)

    print("\nFirst Subject Marks:")
    print(student.subjects[0].marks)


    # Return Student
    # --------------------------------------------------------

    return student
