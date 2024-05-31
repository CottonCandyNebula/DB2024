from pymongo import MongoClient

# •Вывести список студентов для поздравления по месяцам в формате Фамилия И.О., день и название месяца рождения, номером группы и направлением обучения.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

students = db.Students
groups = db.GroupStud
directions = db.Direction

pipeline = [
    {"$match": {"id_group": {"$exists": True}}},
    {"$lookup": {
        "from": "GroupStud",
        "localField": "id_group",
        "foreignField": "id",
        "as": "group_info"
    }},
    {"$unwind": "$group_info"},
    {"$lookup": {
        "from": "Direction",
        "localField": "group_info.direction_id",
        "foreignField": "id",
        "as": "direction_info"
    }},
    {"$unwind": "$direction_info"},
    {"$project": {
        "Студент": {
            "$concat": [
                {"$arrayElemAt": [{"$split": ["$name", ' ']}, 0]},
                " ",
                {"$arrayElemAt": [{"$split": [{"$arrayElemAt": [{"$split": ["$name", ' ']}, 1]}, ' ']}, 0]},
                ". ",
                {"$arrayElemAt": [{"$split": [{"$arrayElemAt": [{"$split": ["$name", ' ']}, 2]}, ' ']}, 0]},
                "."
            ]
        },
        "День": {"$dayOfMonth": "$date_of_birth"},
        "Месяц": {
            "$switch": {
                "branches": [
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 1]}, "then": "Январь"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 2]}, "then": "Февраль"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 3]}, "then": "Март"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 4]}, "then": "Апрель"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 5]}, "then": "Май"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 6]}, "then": "Июнь"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 7]}, "then": "Июль"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 8]}, "then": "Август"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 9]}, "then": "Сентябрь"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 10]}, "then": "Октябрь"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 11]}, "then": "Ноябрь"},
                    {"case": {"$eq": [{"$month": "$date_of_birth"}, 12]}, "then": "Декабрь"}
                ],
                "default": "Неизвестный месяц"
            }
        },
        "Группа": "$group_info.designation",
        "Направление": "$direction_info.title"
    }},
    {"$sort": {"Месяц": 1}}
]

result = students.aggregate(pipeline)

for doc in result:
    print(doc)