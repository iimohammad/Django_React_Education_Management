from django.contrib import admin
from dashboard_student_amirabbas.models import *

class AddRemoveRequestAdmin(admin.ModelAdmin):
    list_display = ('removed_courses', 'added_courses',)
    save_as = True
    list_per_page = 10
    list_max_show_all = 50
admin.site.register(AddRemoveRequest, AddRemoveRequestAdmin)

class EmergencyRemovalRequestAdmin(admin.ModelAdmin):
    list_display = ('course', 'student_explanation', 'educational_assistant_explanation')
    search_fields = ('student_explanation', 'educational_assistant_explanation')
    search_help_text = "Search in: Student Explanation, Educational Assistant Explanation"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(EmergencyRemovalRequest, EmergencyRemovalRequestAdmin)

class CourseRegistrationCancellationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'cancelled' , 'student_explanation', 'educational_assistant_explanation')
    search_fields = ('student_explanation', 'educational_assistant_explanation')
    search_help_text = "Search in: Student Explanation, Educational Assistant Explanation"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(EmergencyRemovalRequest, EmergencyRemovalRequestAdmin)
