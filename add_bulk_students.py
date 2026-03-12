import requests
import random

API_URL = "https://humble-enigma-4j5qj5qxj5jg2q9q5-8000.app.github.dev/add_marks"

headers = {
    "api-key": "teacher123"
}

students = [
    "Rahul","Aman","Deepak","Rohit","Arjun","Vikas","Karan","Sahil","Mohit","Ankit",
    "Ramesh","Suresh","Naresh","Mahesh","Raj","Ajay","Vijay","Sanjay","Pankaj","Tarun",
    "Nikhil","Manish","Yogesh","Lokesh","Harish","Kapil","Vinay","Rajat","Sachin","Varun",
    "Gaurav","Shivam","Prakash","Mukesh","Ravi","Sunil","Kunal","Hemant","Dev","Aditya"
]

subjects = [
    "Math",
    "Physics",
    "Chemistry",
    "English",
    "Computer",
    "Biology"
]

for student in students:
    for subject in subjects:

        data = {
            "name": student,
            "subject": subject,
            "marks": random.randint(40,100)
        }

        r = requests.post(API_URL, json=data, headers=headers)

        print(student, subject, r.json())
