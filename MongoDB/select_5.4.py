from pymongo import MongoClient

# • Определить долю сдавших студентов по каждой дисциплине ("нет оценки" или "2" считать не сдавшими)

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
        '$match': {
            'mark': {'$gt': 2}
        }
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
        '$project': {
            '_id': 0,
            'Предмет': '$_id',
            'Кол-во сдавших': '$count'
        }
    }
]

results = list(db.Marks.aggregate(pipeline))

for result in results:
    print(f"Предмет: {result['Предмет']}, Кол-во сдавших: {result['Кол-во сдавших']}")
