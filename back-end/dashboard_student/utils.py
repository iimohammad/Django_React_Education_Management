from education.models import StudentCourse

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
    student_courses = StudentCourse.objects.filter(student=desired_student,)
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
    grade_of_student=gpa_catergory(desired_student.gpa)
    max_credit = GPA_Dic[grade_of_student]
    credit_until_now=calculate_credit_Course_Semester(desired_student)
    remain_credit = max_credit-credit_until_now
    return remain_credit