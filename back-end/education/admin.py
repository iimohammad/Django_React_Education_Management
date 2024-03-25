from django.contrib import admin
from education.models import *
from import_export.admin import ImportExportActionModelAdmin
from education.resource import *
from django.utils.html import format_html


class SemesterUnitSelectionInline(admin.StackedInline):
    model = SemesterUnitSelection
    can_delete = False
    verbose_name_plural = 'Semester Unit Selection'
    fk_name = 'semester'
    extra = 1


class SemesterClassInline(admin.StackedInline):
    model = SemesterClass
    can_delete = True
    verbose_name_plural = 'Semester Class'
    fk_name = 'semester'
    extra = 2


class SemesterAddRemoveInline(admin.StackedInline):
    model = SemesterAddRemove
    can_delete = False
    verbose_name_plural = 'Semester Add & Remove'
    fk_name = 'semester'
    extra = 3


class SemesterExamInline(admin.StackedInline):
    model = SemesterExam
    can_delete = True
    verbose_name_plural = 'Semester Exam'
    fk_name = 'semester'
    extra = 4


class SemesterEmergencyInline(admin.StackedInline):
    model = SemesterEmergency
    can_delete = False
    verbose_name_plural = 'Semester Emergency'
    fk_name = 'semester'
    extra = 5


class DepartmentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('department_name', 'department_code', 'year_established', 'department_location')
    sortable_by = ('department_code',)
    # readonly_fields = ('department_code',)
    ordering = ('year_established',)
    search_fields = ('department_name', 'year_established')
    search_help_text = "Search in: Department Name, Year of Establishment"
    resource_class = DepartmentResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Department, DepartmentAdmin)


class CourseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'credit_num', 'prerequisite_link', 'corequisite_link')
    sortable_by = ('course_name',)
    # readonly_fields = ('course_code',)
    search_fields = ('course_name', 'credit_num')
    search_help_text = "Search in: Course Name, Credit Number"
    list_display_links = ('course_name', 'prerequisite_link', 'corequisite_link')
    resource_class = CourseResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def prerequisite_link(self, obj):
        prerequisite_id = obj.prerequisite.id
        prerequisite_url = f"http://127.0.0.1:8000/ITM/education/course/{prerequisite_id}/change/"
        return format_html('<a href="{}">{}</a>', prerequisite_url, obj.prerequisite)
    prerequisite_link.short_description = "Prerequisite"

    def corequisite_link(self, obj):
        corequisite_id = obj.corequisite.id
        corequisite_url = f"http://127.0.0.1:8000/ITM/education/course/{corequisite_id}/change/"
        return format_html('<a href="{}">{}</a>', corequisite_url, obj.corequisite)
    corequisite_link.short_description = "Corequisite"

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
    inlines = (SemesterUnitSelectionInline, SemesterClassInline,
               SemesterAddRemoveInline, SemesterExamInline, SemesterEmergencyInline)
    list_display = ('name', 'start_semester', 'end_semester', 'semester_type')
    list_editable = ('semester_type',)
    search_fields = ('name',)
    search_help_text = "Search in: Semester Name"
    resource_class = SemesterResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Semester, SemesterAdmin)


class SemesterCourseAdmin(admin.ModelAdmin):
    list_display = ('semester', 'course', 'class_days', 'class_time', 'instructor', 'course_capacity')
    list_filter = ('class_days',)
    sortable_by = ('course_capacity',)
    search_fields = ('semester', 'course', 'instructor')
    search_help_text = "Search in: Semester Name, Course Name, Instructor Name"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(SemesterCourse, SemesterCourseAdmin)


class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'score')
    list_filter = ('status',)
    sortable_by = ('score',)
    search_fields = ('semester', 'course')
    search_help_text = "Search in: Semester Name, Course Name"
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(StudentCourse, StudentCourseAdmin)
