from pymongo import MongoClient
from datetime import datetime

# •Вывести студентов с указанием возраста в годах

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

students = db.Students

currentYear = datetime.now().year
studentsWithAge = students.aggregate([
    {
        "$project": {
            "name": 1,
            "age": {
                "$subtract": [
                    currentYear,
                    {"$year": "$date_of_birth"}
                ]
            }
        }
    }
])

for student in studentsWithAge:
    print(student)
