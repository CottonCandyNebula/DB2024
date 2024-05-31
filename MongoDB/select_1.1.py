from pymongo import MongoClient

# • Вывести списки групп по заданному направлению с указанием номера группы в формате ФИО, бюджет/внебюджет. Студентов выводить в алфавитном порядке.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

# Коллекция
students = db.Students
#groups = db.GroupStud

# Последовательность
pipeline = [
    {"$lookup": { # соединение коллекций
        "from": "GroupStud",
        "localField": "id_group",
        "foreignField": "id",
        "as": "group_info"
    }},
    {"$unwind": "$group_info"}, # массив информации из коллекции
    {"$project": { #формирование поля и сортировка
        "Студент": "$name",
        "Группа": "$group_info.designation",
        "Место": {"$cond": [{"$eq": ["$budget_place", True]}, "Бюджет", "Внебюджет"]}
    }},
    {"$sort": {"Студент": 1}}
]

result = list(students.aggregate(pipeline))

for doc in result:
    print(doc)
