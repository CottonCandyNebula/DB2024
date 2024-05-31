from pymongo import MongoClient

# • Определить сколько студентов обучатся у каждого их преподавателей.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

pipeline = [
    {"$lookup": {"from": "Teachers_and_subjects", "localField": "id", "foreignField": "teacher_id", "as": "teacher_subject"}},
    {"$unwind": "$teacher_subject"},
    {"$lookup": {"from": "Marks", "localField": "teacher_subject.id", "foreignField": "tas_id", "as": "marks"}},
    {"$unwind": "$marks"},
    {"$group": {"_id": "$teacher_subject.teacher_id", "teacher_name": {"$first": "$teacher_subject.teacher_id"}, "count_students": {"$sum": 1}}},
    {"$lookup": {"from": "Teachers", "localField": "teacher_name", "foreignField": "id", "as": "teacher"}},
    {"$project": {"_id": 0, "Преподаватель": "$teacher.name_t", "Кол-во студентов": "$count_students"}}
]

results = db.Students.aggregate(pipeline)

#for doc in result:
#    print(doc)

for result in results:
    #print(result)
    print(f"Преподаватель: {result['Преподаватель']}, Кол-во студентов: {result['Кол-во студентов']}")