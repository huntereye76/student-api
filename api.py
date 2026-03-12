from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    marks INTEGER
)
""")
conn.commit()


class Student(BaseModel):
    name: str
    subject: str
    marks: int


TEACHER_KEY = "teacher123"


# Teacher adds marks
@app.post("/add_marks")
def add_marks(student: Student, api_key: str = Header(None)):

    if api_key != TEACHER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cursor.execute(
        "INSERT INTO students (name, subject, marks) VALUES (?, ?, ?)",
        (student.name, student.subject, student.marks),
    )

    conn.commit()

    return {"message": "Marks added"}


# Students check marks
@app.get("/marks/{name}")
def get_marks(name: str):

    # cursor.execute("SELECT subject, marks FROM students WHERE name=?", (name,))
    cursor.execute(
        "SELECT subject, marks FROM students WHERE LOWER(name)=LOWER(?)",
        (name,)
    )
    rows = cursor.fetchall()

    if not rows:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"name": name, "marks": rows}



@app.get("/all")
def all_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()



@app.get("/students")
def all_students():
    cursor.execute("SELECT DISTINCT name FROM students")
    rows = cursor.fetchall()

    students = [row[0] for row in rows]

    return {"students": students}



@app.put("/update_marks")
def update_marks(student: Student, api_key: str = Header(None)):

    if api_key != TEACHER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cursor.execute(
        "UPDATE students SET marks=? WHERE name=? AND subject=?",
        (student.marks, student.name, student.subject)
    )

    conn.commit()

    return {"message": "Marks updated"}



@app.delete("/delete_student/{name}")
def delete_student(name: str, api_key: str = Header(None)):

    if api_key != TEACHER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cursor.execute("DELETE FROM students WHERE name=?", (name,))
    conn.commit()

    return {"message": f"{name} deleted"}



@app.delete("/delete_subject")
def delete_subject(student: Student, api_key: str = Header(None)):

    if api_key != TEACHER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cursor.execute(
        "DELETE FROM students WHERE name=? AND subject=?",
        (student.name, student.subject)
    )

    conn.commit()

    return {"message": "Subject removed"}



@app.get("/subjects/{name}")
def subjects(name: str):

    cursor.execute(
        "SELECT subject FROM students WHERE LOWER(name)=LOWER(?)",
        (name,)
    )

    rows = cursor.fetchall()

    return {"name": name, "subjects": [r[0] for r in rows]}





# Get leaderboard (top students by average marks)
@app.get("/leaderboard")
def leaderboard():

    cursor.execute("""
        SELECT name, AVG(marks) as avg_marks
        FROM students
        GROUP BY name
        ORDER BY avg_marks DESC
    """)

    rows = cursor.fetchall()

    leaderboard_list = [
        {"name": row[0], "average_marks": round(row[1], 2)}
        for row in rows
    ]

    return {"leaderboard": leaderboard_list}


# Get average marks of one student
@app.get("/student/{name}/average")
def student_average(name: str):

    cursor.execute(
        """
        SELECT AVG(marks)
        FROM students
        WHERE LOWER(name) = LOWER(?)
        """,
        (name,)
    )

    row = cursor.fetchone()

    if row[0] is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "name": name,
        "average_marks": round(row[0], 2)
    }


# Get class average
@app.get("/class_average")
def class_average():

    cursor.execute("SELECT AVG(marks) FROM students")

    row = cursor.fetchone()

    return {
        "class_average": round(row[0], 2)
    }
