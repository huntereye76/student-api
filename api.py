from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import sqlite3

# Create FastAPI app
app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    marks INTEGER
)
""")
conn.commit()


# Data model for student input
class Student(BaseModel):
    name: str
    subject: str
    marks: int


# Teacher API Key
TEACHER_KEY = "teacher123"


# -------------------------------------
# AUTHENTICATION FUNCTION
# -------------------------------------
# This function checks if the teacher API key is correct
# We will reuse this for all teacher-only routes
def verify_teacher(api_key: str = Header(None)):
    if api_key != TEACHER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


# -------------------------------------
# TEACHER ROUTES
# -------------------------------------

# Add marks for a student
@app.post("/add_marks")
def add_marks(student: Student, auth: str = Depends(verify_teacher)):

    cursor.execute(
        "INSERT INTO students (name, subject, marks) VALUES (?, ?, ?)",
        (student.name, student.subject, student.marks)
    )

    conn.commit()

    return {"message": "Marks added"}


# Update marks for a student subject
@app.put("/update_marks")
def update_marks(student: Student, auth: str = Depends(verify_teacher)):

    cursor.execute(
        "UPDATE students SET marks=? WHERE name=? AND subject=?",
        (student.marks, student.name, student.subject)
    )

    conn.commit()

    return {"message": "Marks updated"}


# Delete an entire student record
@app.delete("/delete_student/{name}")
def delete_student(name: str, auth: str = Depends(verify_teacher)):

    cursor.execute(
        "DELETE FROM students WHERE LOWER(name)=LOWER(?)",
        (name,)
    )

    conn.commit()

    return {"message": f"{name} deleted"}


# Delete a specific subject of a student
@app.delete("/delete_subject")
def delete_subject(student: Student, auth: str = Depends(verify_teacher)):

    cursor.execute(
        "DELETE FROM students WHERE name=? AND subject=?",
        (student.name, student.subject)
    )

    conn.commit()

    return {"message": "Subject removed"}


# -------------------------------------
# PUBLIC STUDENT ROUTES
# -------------------------------------

# Get marks of a specific student
@app.get("/marks/{name}")
def get_marks(name: str):

    cursor.execute(
        "SELECT subject, marks FROM students WHERE LOWER(name)=LOWER(?)",
        (name,)
    )

    rows = cursor.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"name": name, "marks": rows}


# Get list of all students
@app.get("/students")
def students():

    cursor.execute("SELECT DISTINCT name FROM students")

    rows = cursor.fetchall()

    students_list = [row[0] for row in rows]

    return {"students": students_list}


# Get subjects studied by a student
@app.get("/subjects/{name}")
def subjects(name: str):

    cursor.execute(
        "SELECT subject FROM students WHERE LOWER(name)=LOWER(?)",
        (name,)
    )

    rows = cursor.fetchall()

    return {
        "name": name,
        "subjects": [r[0] for r in rows]
    }


# -------------------------------------
# ANALYTICS ROUTES
# -------------------------------------

# Get leaderboard sorted by average marks
@app.get("/leaderboard")
def leaderboard():

    cursor.execute("""
        SELECT name, AVG(marks)
        FROM students
        GROUP BY name
        ORDER BY AVG(marks) DESC
    """)

    rows = cursor.fetchall()

    leaderboard_list = [
        {"name": row[0], "average_marks": round(row[1], 2)}
        for row in rows
    ]

    return {"leaderboard": leaderboard_list}


# Get average marks of a specific student
@app.get("/student/{name}/average")
def student_average(name: str):

    cursor.execute(
        "SELECT AVG(marks) FROM students WHERE LOWER(name)=LOWER(?)",
        (name,)
    )

    row = cursor.fetchone()

    if row[0] is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "name": name,
        "average_marks": round(row[0], 2)
    }


# Get average marks of entire class
@app.get("/class_average")
def class_average():

    cursor.execute("SELECT AVG(marks) FROM students")

    row = cursor.fetchone()

    return {
        "class_average": round(row[0], 2)
    }
