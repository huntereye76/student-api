# 🎓 Student Marks REST API

Simple REST API built with **FastAPI** to store and retrieve student marks.

This project demonstrates:

* REST API fundamentals
* Header-based authentication
* SQLite database integration
* Public API testing via GitHub Codespaces
* CRUD operations
* Basic analytics (leaderboard and averages)

---

# 🚀 Base URL

```
https://your-codespace-url-8000.app.github.dev
```

Example:

```
https://humble-enigma-xxxx-8000.app.github.dev
```

---

# 📚 API Endpoints

## 🔹 Student Information

### Get All Students

```
GET /students
```

Returns a list of all unique students.

Example Response

```json
{
  "students": ["Rahul","Aman","Deepak","Rohit"]
}
```

---

### Get Student Marks

```
GET /marks/{name}
```

Example

```
GET /marks/Rahul
```

Response

```json
{
  "name": "Rahul",
  "marks": [
    ["Math", 90],
    ["Physics", 85]
  ]
}
```

---

### Get Student Subjects

```
GET /subjects/{name}
```

Example Response

```json
{
  "name": "Rahul",
  "subjects": ["Math","Physics","English"]
}
```

---

# 🧮 Analytics Endpoints

### Leaderboard

Returns all students ranked by average marks.

```
GET /leaderboard
```

Example Response

```json
{
  "leaderboard": [
    {"name": "Rahul", "average_marks": 92.4},
    {"name": "Aman", "average_marks": 89.7}
  ]
}
```

---

### Student Average

```
GET /student/{name}/average
```

Example

```
GET /student/Rahul/average
```

Response

```json
{
  "name": "Rahul",
  "average_marks": 91.3
}
```

---

### Class Average

```
GET /class_average
```

Example Response

```json
{
  "class_average": 84.6
}
```

---

### Topper

```
GET /topper
```

Example Response

```json
{
  "topper": "Rahul",
  "average_marks": 92.5
}
```

---

# ✏ Teacher Operations

Teacher endpoints require authentication.

### Add Marks

```
POST /add_marks
```

Header

```
api-key: teacher123
```

Body

```json
{
  "name": "Rahul",
  "subject": "Math",
  "marks": 90
}
```

Response

```json
{
  "message": "Marks added"
}
```

---

### Update Marks

```
PUT /update_marks
```

Body

```json
{
  "name": "Rahul",
  "subject": "Math",
  "marks": 95
}
```

---

### Delete Student

```
DELETE /delete_student/{name}
```

Example

```
DELETE /delete_student/Rahul
```

---

### Delete Subject

```
DELETE /delete_subject
```

Body

```json
{
  "name": "Rahul",
  "subject": "Math"
}
```

---

# 🔐 Authentication

Teacher endpoints require a header:

```
api-key: teacher123
```

If the key is incorrect the API returns:

```json
{
  "detail": "Unauthorized"
}
```

---

# 🗄 Database

The project uses **SQLite**.

The database file is created automatically:

```
database.db
```

Table structure:

| Column  | Type    |
| ------- | ------- |
| id      | INTEGER |
| name    | TEXT    |
| subject | TEXT    |
| marks   | INTEGER |

---

# 🧪 Testing the API

You can test the API using:

* Browser
* Python requests
* Swagger UI

Swagger documentation:

```
/docs
```

Example

```
https://your-api-url/docs
```

---

# 📦 Requirements

```
fastapi
uvicorn
pydantic
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# ▶ Run the Server

```
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

---

# 🌍 Public Testing

When running in **GitHub Codespaces**, the API automatically becomes publicly accessible via forwarded ports.

---

# 📌 Future Improvements

Possible upgrades:

* JWT authentication
* Student login system
* Pagination for leaderboard
* PostgreSQL database
* Docker deployment
* Rate limiting
* Role-based authentication

---

# 👨‍💻 Learning Goal

This project demonstrates how real backend REST APIs work.

Concepts covered:

* API routing
* HTTP methods (GET, POST, PUT, DELETE)
* Header authentication
* Database interaction
* Data analytics with SQL

Feel free to fork, extend, and experiment with it.
