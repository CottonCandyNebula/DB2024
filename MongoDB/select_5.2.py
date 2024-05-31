from pymongo import MongoClient

# • Определить, какую дисциплину изучает максимальное количество студентов.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

pipeline = [
    {
        '$lookup': {
            'from': 'Teachers_and_subjects',
            'localField': 'tas_id',
            'foreignField': 'id',
            'as': 'teacher_subject'
        }
    },
    {
        '$unwind': '$teacher_subject'
    },
    {
        '$lookup': {
            'from': 'Subjects',
            'localField': 'teacher_subject.subject_id',
            'foreignField': 'id',
            'as': 'subject'
        }
    },
    {
        '$unwind': '$subject'
    },
    {
        '$group': {
            '_id': '$subject.subject',
            'count': {'$sum': 1}
        }
    },
    {
        '$sort': {
            'count': -1
        }
    },
    {
        '$limit': 1
    },
    {
        '$project': {
            '_id': 0,
            'Дисциплина': '$_id',
            'Сколько студентов изучает': '$count'
        }
    }
]

result = db.Marks.aggregate(pipeline).next()
print(result)

