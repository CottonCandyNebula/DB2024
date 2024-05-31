from pymongo import MongoClient

# • Для каждого студента вывести общее время, потраченное на изучение каждого предмета.

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]

pipeline = [
    {
        '$match': {
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
        '$lookup': {
            'from': 'Students',
            'localField': 'stud_id',
            'foreignField': 'id',
            'as': 'student'
        }
    },
    {
        '$unwind': '$student'
    },
    {
        '$group': {
            '_id': {
                'student_id': '$student.id',
                'subject_id': '$subject.id'
            },
            'total_time': {
                '$sum': 1.5
            }
        }
    },
    {
        '$lookup': {
            'from': 'Students',
            'localField': '_id.student_id',
            'foreignField': 'id',
            'as': 'student'
        }
    },
    {
        '$unwind': '$student'
    },
    {
        '$lookup': {
            'from': 'Subjects',
            'localField': '_id.subject_id',
            'foreignField': 'id',
            'as': 'subject'
        }
    },
    {
        '$unwind': '$subject'
    },
    {
        '$project': {
            '_id': 0,
            'Студент': '$student.name',
            'Предмет': '$subject.subject',
            'Общее время изучения предмета': '$total_time'
        }
    }
]

results = list(db.Attendance.aggregate(pipeline))
for result in results:
    print(f"Студент: {result['Студент']}, Предмет: {result['Предмет']}, Общее время изучения предмета: {result['Общее время изучения предмета']}")