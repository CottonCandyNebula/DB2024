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
            'from': 'Direction',
            'localField': 'teacher_subject.direction_id',
            'foreignField': 'id',
            'as': 'direction'
        }
    },
    {
        '$unwind': '$direction'
    },
    {
        '$lookup': {
            'from': 'GroupStud',
            'localField': 'direction.id',
            'foreignField': 'direction_id',
            'as': 'group'
        }
    },
    {
        '$unwind': '$group'
    },
    {
        '$group': {
            '_id': '$group.designation',
            'avg_mark': {'$avg': '$mark'}
        }
    },
    {
        # сортировка в порядке убывания по средней оценке
        '$sort': {
            'avg_mark': -1
        }
    },
    {
        '$limit': 1
    },
    {
        '$project': {
            '_id': 0,
            'Группа': '$_id',
            'Максимальная оценка': {'$round': ['$avg_mark', 2]}
        }
    }
]

result = db.Marks.aggregate(pipeline).next()
print(result)