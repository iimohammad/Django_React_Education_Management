from django.contrib import admin
from education.models import Department, Course, Major, Semester, SemesterCourse, StudentCourse
from import_export.admin import ImportExportActionModelAdmin
from education.resource import *
from datetime import timedelta
from django.utils.html import format_html


class DepartmentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'year_established', 'number_of_students')
    sortable_by = ('department_code', 'number_of_students')
    # readonly_fields = ('department_code',)
    ordering = ('year_established',)
    search_fields = ('department_name', 'year_established')
    search_help_text = "Search in: Department Name, Year of Establishment"
    resource_class = DepartmentResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    actions = ['increment_ten_students']

    def increment_ten_students(self, request, queryset):
        for department in queryset:
            student_count = department.number_of_students + 10
            department.number_of_students = student_count
            department.save()

    increment_ten_students.short_description = "Increase the selected departments' student capacity by 10"

admin.site.register(Department, DepartmentAdmin)


class CourseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'credit_num')
    sortable_by = ('course_name',)
    # readonly_fields = ('course_code',)
    search_fields = ('course_name', 'credit_num')
    search_help_text = "Search in: Course Name, Credit Number"
    resource_class = CourseResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Course, CourseAdmin)


class MajorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('major_name', 'major_code', 'department_link', 'level', 'education_group')
    list_filter = ('department', 'level', 'education_group')
    sortable_by = ('department', 'level')
    list_editable = ('level',)
    # readonly_fields = ('major_code',)
    search_fields = ('major_name', 'department_link', 'education_group')
    search_help_text = "Search in: Major Name, Department, Education Group"
    list_display_links = ('major_name', 'department_link')
    resource_class = MajorResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def department_link(self, obj):
        department_id = obj.department.id
        department_url = f"http://127.0.0.1:8000/ITM/education/department/{department_id}/change/"
        return format_html('<a href="{}">{}</a>', department_url, obj.department)
    department_link.short_description = "Department"

admin.site.register(Major, MajorAdmin)


class SemesterAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'start_semester', 'end_semester', 'exam_start', 'exam_end')
    list_editable = ('exam_start', 'exam_end')
    search_fields = ('name',)
    search_help_text = "Search in: Semester Name"
    resource_class = SemesterResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    actions = ['extend_exam_duration_for_three_days']

    def extend_exam_duration_for_three_days(self, request, queryset):
        for semester in queryset:
            new_exam_end = semester.exam_end + timedelta(days=3)
            semester.exam_end = new_exam_end
            semester.save()

    extend_exam_duration_for_three_days.short_description = "Extend exam duration \
                                                    for the selected semesters by three days"

admin.site.register(Semester, SemesterAdmin)

admin.site.register(SemesterCourse)
admin.site.register(StudentCourse)