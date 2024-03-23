from django.contrib import admin
from .models import Teacher, Student, EducationalAssistant, User

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(EducationalAssistant)
admin.site.register(User)