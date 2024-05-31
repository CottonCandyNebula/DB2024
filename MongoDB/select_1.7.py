from pymongo import MongoClient

# •Вывести количество бюджетных и внебюджетных мест по группам. Для каждой группы вывести номер и название направления.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

students = db['Students']
group_stud = db['GroupStud']
direction = db['Direction']

pipeline = [
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
    {"$group": {
        "_id": {
            "Группа": "$group_info.designation",
            "Направление": "$direction_info.title"
        },
        "Кол-во бюджетных мест": {"$sum": {"$cond": [{"$eq": ["$budget_place", True]}, 1, 0]}},
        "Кол-во внебюджетных мест": {"$sum": {"$cond": [{"$eq": ["$budget_place", False]}, 1, 0]}}
    }},
    {"$project": {
        "_id": 0,
        "Группа": "$_id.Группа",
        "Направление": "$_id.Направление",
        "Кол-во бюджетных мест": 1,
        "Кол-во внебюджетных мест": 1
    }}
]

result = students.aggregate(pipeline)

for doc in result:
    print(f"Группа: {doc['Группа']}, Направление: {doc['Направление']}, Кол-во бюджетных мест: {doc['Кол-во бюджетных мест']}, Кол-во внебюджетных мест: {doc['Кол-во внебюджетных мест']}")

