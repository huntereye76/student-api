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
