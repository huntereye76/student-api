# 🎓 Student Marks REST API

Simple REST API built with **FastAPI** to store and retrieve student marks.

This project demonstrates:

* REST API basics
* Header authentication
* SQLite database usage
* Public API testing

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

## 1️⃣ Add Marks (Teacher Only)

Add student marks into the database.

### Endpoint

```
POST /add_marks
```

### Headers

```
api-key: teacher123
```

### Body

```json
{
  "name": "Rahul",
  "subject": "Math",
  "marks": 90
}
```

### Example using Python

```python
import requests

url = "https://your-api-url/add_marks"

data = {
    "name": "Rahul",
    "subject": "Math",
    "marks": 90
}

headers = {
    "api-key": "teacher123"
}

r = requests.post(url, json=data, headers=headers)

print(r.json())
```

### Response

```json
{
  "message": "Marks added"
}
```

---

# 2️⃣ Check Student Marks

Students can check their marks.

### Endpoint

```
GET /marks/{name}
```

### Example

```
GET /marks/Rahul
```

### Example using Python

```python
import requests

url = "https://your-api-url/marks/Rahul"

r = requests.get(url)

print(r.json())
```

### Response

```json
{
  "name": "Rahul",
  "marks": [
    ["Math", 90]
  ]
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

This project uses **SQLite**.

The database file is automatically created:

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

Example:

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

Install:

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

When running in GitHub Codespaces the API becomes public automatically via forwarded ports.

---

# 📌 Future Improvements

Possible extensions:

* Student login system
* JWT authentication
* Update marks endpoint
* Delete student endpoint
* Leaderboard API
* PostgreSQL database

---

# 👨‍💻 Learning Goal

This project is built for learning how real **REST APIs** work.

Feel free to fork and extend it.
