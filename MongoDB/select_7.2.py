from pymongo import MongoClient

# •Вывести по заданному предмету количество пропущенных занятий.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

attendance = db.Attendance
study_schedule = db.Study_schedule
subjects = db.Subjects

pipeline = [
    {"$lookup": {
        "from": "Study_schedule",
        "localField": "schedule_id",
        "foreignField": "id",
        "as": "schedule_info"
    }},
    {"$lookup": {
        "from": "Subjects",
        "localField": "schedule_info.subj_id",
        "foreignField": "id",
        "as": "subject_info"
    }},
    {"$unwind": "$schedule_info"},
    {"$unwind": "$subject_info"},
    {"$match": {
        "subject_info.subject": "Higher Mathematics",  # ПРЕДМЕТ
        "attend": 0  # фильтруется по отметке
    }},
    {"$group": {
        "_id": "$subject_info.subject",
        "Пропуски предмета студентами": {"$sum": 1}
    }},
    {"$project": {
        "_id": 0,
        "Предмет": "$_id",
        "Пропуски предмета студентами": "$Пропуски предмета студентами"
    }}
]

results = attendance.aggregate(pipeline)

for result in results:
    print(f"Предмет: {result['Предмет']}, Пропуски предмета студентами: {result['Пропуски предмета студентами']}")