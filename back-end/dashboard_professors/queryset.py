from accounts.models import Student, User

def get_student_queryset(request):
    if isinstance(request.user, User):
        user_id = request.user
    else:
        user_id = request.user.id

    return Student.objects.filter(advisor__user=user_id)
