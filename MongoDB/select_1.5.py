from pymongo import MongoClient
from datetime import datetime

# •Вывести студентов, у которых день рождения в текущем месяце.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

students = db.Students

current_month = datetime.now().month

results = students.find({"$expr": {"$eq": [{"$month": "$date_of_birth"}, current_month]}})

for result in results:
    print("Студент:", result['name'])
    print("Дата рождения (этот месяц):", result['date_of_birth'])