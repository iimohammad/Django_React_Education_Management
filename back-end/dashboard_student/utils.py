import redis
from accounts.models import Student
from config import settings
from education.models import Semester, SemesterCourse, StudentCourse

GPA_Dic = {
    'A' : 24,
    'B': 18,
    'C': 14,
    'D':12,
    'N':17,
}

def gpa_catergory(student_gpa):
    if student_gpa >= 17:
        return 'A'
    
    if student_gpa<17 and student_gpa>=14:
        return 'B'
    
    if student_gpa<14 and student_gpa>=12:
        return 'C'
    
    if student_gpa<12:
        return 'D'
    else:
        return 'N'
    


def calculate_credit_Course_Semester(desired_student):
    last_semester = last_semester = Semester.objects.order_by('-start_semester').first()
    student_courses = StudentCourse.objects.filter(student=desired_student,
                                                   semester_course__semester = last_semester)
    total_credit = 0
    # Iterate through each StudentCourse and sum up the credit numbers of the associated courses
    for student_course in student_courses:
        # Get the associated SemesterCourse and retrieve its course's credit number
        course_credit = student_course.semester_course.course.credit_num
        
        # Add the credit number to the total
        total_credit += course_credit
    
    # Return the total credit
    return total_credit


def find_remain_credit(desired_student):
    if desired_student.gpa is None:
        grade_of_student = 'N'
    else:
        grade_of_student=gpa_catergory(desired_student.gpa)
    max_credit = GPA_Dic[grade_of_student]
    credit_until_now=calculate_credit_Course_Semester(desired_student)
    remain_credit = max_credit-credit_until_now
    return remain_credit




def save_to_redis(course_id, user_id):
    redis_instance = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    if not redis_instance.sismember(f"course_{course_id}_requests", user_id):
        redis_instance.sadd(f"course_{course_id}_requests", user_id)


def add_from_redis_to_database(course_id):
    redis_instance = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    
    while redis_instance.llen(f"course_{course_id}_requests") > 0:
        user_id = redis_instance.rpop(f"course_{course_id}_requests")
        
        student = Student.objects.get(user_id=user_id)
        request_course = SemesterCourse.objects.get(id=course_id)
        
        StudentCourse.objects.create(
            student=student,
            semester_course=request_course,
            status='R',
        )