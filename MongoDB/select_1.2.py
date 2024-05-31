from pymongo import MongoClient

# • Вывести студентов с фамилией, начинающейся с первой буквы вашей фамилии, с указанием ФИО, номера группы и направления обучения.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

students = db.Students
group_stud = db.GroupStud
direction = db.Direction

result = list(students.aggregate([
    {
        "$match": {
            "name": {"$regex": "^K"}  # Фильтруем студентов по имени, начинающемуся с 'К'
        }
    },
    {
        "$lookup": {
            "from": "GroupStud",
            "localField": "id_group",
            "foreignField": "id",
            "as": "group_info"
        }
    },
    {
        "$lookup": {
            "from": "Direction",
            "localField": "group_info.direction_id",
            "foreignField": "id",
            "as": "direction_info"
        }
    },
    {
        "$unwind": "$group_info"
    },
    {
        "$unwind": "$direction_info"
    },
    {
        "$project": {
            "name": 1,
            "group_info.designation": 1,
            "direction_info.title": 1
        }
    }
]))


for doc in result:
    print(doc)
