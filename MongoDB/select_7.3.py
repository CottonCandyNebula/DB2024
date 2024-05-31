from pymongo import MongoClient

# •Вывести по заданному преподавателю количество студентов на каждом занятии.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

teacher_id = 5  # айдишник преподавателя

pipeline = [
    {
        '$match': {
            'teach_id': teacher_id,
            'attend': 1
        }
    },
    {
        '$lookup': {
            'from': 'Study_schedule',
            'localField': 'schedule_id',
            'foreignField': 'id',
            'as': 'schedule'
        }
    },
    {
        '$unwind': '$schedule'
    },
    {
        '$lookup': {
            'from': 'Teachers_and_subjects',
            'localField': 'schedule.subj_id',
            'foreignField': 'id',
            'as': 'teacher_subject'
        }
    },
    {
        '$unwind': '$teacher_subject'
    },
    {
        '$lookup': {
            'from': 'Teachers',
            'localField': 'teacher_subject.teacher_id',
            'foreignField': 'id',
            'as': 'teacher'
        }
    },
    {
        '$unwind': '$teacher'
    },
    {
        '$group': {
            '_id': {
                'teacher_id': '$teacher.id',
                'schedule_id': '$schedule.id',
                'date_lesson': '$schedule.date_lesson'
            },
            'count': {'$sum': 1}
        }
    },
    {
        '$project': {
            '_id': 0,
            'Преподаватель': '$_id.teacher_id',
            'Дата занятия': '$_id.date_lesson',
            'Количество студентов': '$count'
        }
    }
]

results = list(db.Attendance.aggregate(pipeline))

for result in results:
    print(f"Преподаватель: {result['Преподаватель']}, Дата занятия: {result['Дата занятия']}, Количество студентов: {result['Количество студентов']}")