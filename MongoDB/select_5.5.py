from pymongo import MongoClient

# • Определить среднюю оценку по предметам (для сдавших студентов)

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
            'mark': {'$gt': 0}
        }
    },
    {
        '$group': {
            '_id': '$subject.subject',
            'avg_mark': {'$avg': '$mark'}
        }
    },
    {
        # сортировка по предметам
        '$sort': {
            '_id': 1
        }
    },
    {
        '$project': {
            '_id': 0,
            'Предмет': '$_id',
            'Среднее значение': {'$round': ['$avg_mark', 2]}
        }
    }
]

results = list(db.Marks.aggregate(pipeline))

for result in results:
    print(f"Предмет: {result['Предмет']}, Среднее значение: {result['Среднее значение']}")
