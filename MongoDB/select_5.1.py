from pymongo import MongoClient

# •Вывести списки групп по каждому предмету с указанием преподавателя.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

pipeline = [
    {
        '$lookup': {
            'from': 'Teachers',
            'localField': 'teacher_id',
            'foreignField': 'id',
            'as': 'teacher'
        }
    },
    {
        '$unwind': '$teacher'
    },
    {
        '$lookup': {
            'from': 'Subjects',
            'localField': 'subject_id',
            'foreignField': 'id',
            'as': 'subject'
        }
    },
    {
        '$unwind': '$subject'
    },
    {
        '$lookup': {
            'from': 'GroupStud',
            'localField': 'direction_id',
            'foreignField': 'direction_id',
            'as': 'group'
        }
    },
    {
        '$unwind': '$group'
    },
    {
        '$lookup': {
            'from': 'Direction',
            'localField': 'direction_id',
            'foreignField': 'id',
            'as': 'direction'
        }
    },
    {
        '$unwind': '$direction'
    },
    {
        '$project': {
            '_id': 0,
            'Предмет': '$subject.subject',
            'Преподаватель': '$teacher.name_t',
            'Группа': '$group.designation',
            'Направление': '$direction.title'
        }
    }
]

results = list(db.Teachers_and_subjects.aggregate(pipeline))

for result in results:
    #print(result)
    print(f"Предмет: {result['Предмет']}, Преподаватель: {result['Преподаватель']}, Группа: {result['Группа']}, Направление: {result['Направление']}")