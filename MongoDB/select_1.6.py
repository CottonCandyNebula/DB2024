from pymongo import MongoClient

# •Вывести количество студентов по каждому направлению.

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
        "_id": "$direction_info.title",
        "Количество студентов": {"$sum": 1}
    }},
    {"$sort": {"_id": 1}}
]

result = students.aggregate(pipeline)

for doc in result:
    print(f"Направление: {doc['_id']}, Количество студентов: {doc['Количество студентов']}")
