from django.contrib import admin

from dashboard_student.models import *

admin.site.register(SemesterRegistrationRequest)
admin.site.register(AddRemoveRequest)
admin.site.register(EmploymentEducationRequest)


class RevisionRequestAdmin(admin.ModelAdmin):
    list_display = ('course', 'text', 'answer')
    search_fields = ('text', 'answer')
    search_help_text = "Search in: Text, Answer"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50


admin.site.register(RevisionRequest, RevisionRequestAdmin)

# class AddRemoveRequestAdmin(admin.ModelAdmin):
#     list_display = ('semester', 'approval_status',
#                     'student', 'created_at', 
#                     'added_universities', 'removed_universities ')
#     search_fields = (' added_universities',
#                      'removed_universities ')
#     search_help_text = "Search in: Student Explanation, Educational Assistant Explanation"
#     save_as = True
#     list_per_page = 10
#     list_max_show_all = 50


# admin.site.register(AddRemoveRequest,AddRemoveRequestAdmin)


class EmergencyRemovalRequestAdmin(admin.ModelAdmin):
    list_display = ('course', 'student_explanation',
                    'educational_assistant_explanation')
    search_fields = ('student_explanation',
                     'educational_assistant_explanation')
    search_help_text = "Search in: Student Explanation, Educational Assistant Explanation"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50


admin.site.register(EmergencyRemovalRequest, EmergencyRemovalRequestAdmin)


class StudentDeleteSemesterRequestAdmin(admin.ModelAdmin):
    list_display = ('semester_registration_request', 'teacher_approval_status',
                    'educational_assistant_approval_status', 'created_at', 
                    'student_explanations', 'educational_assistant_explanation')
    search_fields = ('student_explanations',
                     'educational_assistant_explanation')
    search_help_text = "Search in: Student Explanation, Educational Assistant Explanation"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50


admin.site.register(StudentDeleteSemesterRequest,
                    StudentDeleteSemesterRequestAdmin)


class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'approval_status', 'reason_text')
    list_filter = ('approval_status',)
    search_fields = ('teacher', 'reason_text')
    search_help_text = "Search in: Teacher, Reason Text"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50


admin.site.register(EnrollmentRequest, EnrollmentRequestAdmin)