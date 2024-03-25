from django.contrib import admin
from .models import Teacher, Student, EducationalAssistant, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportActionModelAdmin
from .resource import EducationalAssistantResource, StudentResource, TeacherResource, UserResource

@admin.register(User)
class UserAdmin(BaseUserAdmin, ImportExportActionModelAdmin):
    resource_class = UserResource


@admin.register(Teacher)
class TeacherAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
       resource_class = TeacherResource 

@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
       resource_class = StudentResource 

@admin.register(EducationalAssistant)
class StudentAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
       resource_class = EducationalAssistantResource 