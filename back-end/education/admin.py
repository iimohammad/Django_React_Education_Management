# from calendar import Day
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportActionModelAdmin
import os

admin_url = os.environ.get('Admin')
from education.models import (
    Course,
    Department,
    Major,
    Prerequisite,
    Requisite,
    Semester,
    SemesterAddRemove, SemesterClass,
    SemesterCourse,
    SemesterEmergency,
    SemesterExam,
    SemesterUnitSelection,
    StudentCourse,
    Day,
)
from education.resource import (DepartmentResource,
                                MajorResource,
                                CourseResource,
                                SemesterResource,
                                SemesterUnitSelectionResource,
                                SemesterClassResource,
                                SemesterAddRemoveResource,
                                SemesterExamResource,
                                SemesterEmergencyResource,
                                PrerequisiteResource,
                                RequisiteResource,
                                SemesterCourseResource,
                                StudentCourseResource)


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
    list_display = ('id', 'department_name', 'department_code',
                    'year_established', 'department_location')
    sortable_by = ('department_code',)
    ordering = ('year_established',)
    search_fields = ('department_name', 'year_established')
    search_help_text = "Search in: Department Name, Year of Establishment"
    resource_class = DepartmentResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Department, DepartmentAdmin)


class CourseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'course_name', 'department_link', 'major_link',
                    'credit_num', 'course_type', 'availablity')
    list_filter = ('course_type', 'availablity')
    sortable_by = ('course_name', 'credit_num')
    list_editable = ('course_type', 'availablity')
    search_fields = ('course_name', 'credit_num')
    search_help_text = "Search in: Course Name, Credit Number"
    list_display_links = ('course_name', 'department_link', 'major_link')
    resource_class = CourseResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def department_link(self, obj):
        department_id = obj.department.id
        department_url = f"http://127.0.0.1:8000/{admin_url}education/\
        department/{department_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           department_url, obj.department)
    
    def major_link(self, obj):
        major_id = obj.major.id
        major_url = f"http://127.0.0.1:8000/{admin_url}education/\
        major/{major_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           major_url, obj.major)

    department_link.short_description = "Department"
    major_link.short_description = "Major"

admin.site.register(Course, CourseAdmin)


class PrerequisiteAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'course', 'prerequisite')
    resource_class = PrerequisiteResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Prerequisite, PrerequisiteAdmin)


class RequisiteAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'course', 'requisite')
    resource_class = RequisiteResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Requisite, RequisiteAdmin)


class MajorAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'major_name', 'major_code',
                    'department_link', 'level', 'education_group')
    list_filter = ('department', 'level', 'education_group')
    sortable_by = ('department', 'level')
    list_editable = ('level',)
    search_fields = ('major_name', 'department_link', 'education_group')
    search_help_text = "Search in: Major Name, Department, Education Group"
    list_display_links = ('major_name', 'department_link')
    resource_class = MajorResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def department_link(self, obj):
        department_id = obj.department.id
        department_url = f"http://127.0.0.1:8000/{admin_url}education/\
        department/{department_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           department_url, obj.department)

    department_link.short_description = "Department"


admin.site.register(Major, MajorAdmin)


class SemesterAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = (
        SemesterUnitSelectionInline,
        SemesterClassInline,
        SemesterAddRemoveInline,
        SemesterExamInline,
        SemesterEmergencyInline)
    list_display = ('id', 'name', 'start_semester', 'end_semester', 'semester_type')
    list_editable = ('semester_type',)
    search_fields = ('name',)
    search_help_text = "Search in: Semester Name"
    resource_class = SemesterResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(Semester, SemesterAdmin)


class SemesterUnitSelectionAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'semester', 'unit_selection_start', 'unit_selection_end')
    resource_class = SemesterUnitSelectionResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(SemesterUnitSelection, SemesterUnitSelectionAdmin)


class SemesterClassAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'semester', 'classes_start', 'classes_end')
    resource_class = SemesterClassResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(SemesterClass, SemesterClassAdmin)


class SemesterAddRemoveAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'semester', 'addremove_start', 'addremove_end')
    resource_class = SemesterAddRemoveResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(SemesterAddRemove, SemesterAddRemoveAdmin)


class SemesterExamAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'semester', 'exam_start', 'exam_end')
    resource_class = SemesterExamResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(SemesterExam, SemesterExamAdmin)


class SemesterEmergencyAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'semester', 'emergency_remove_start', 'emergency_remove_end')
    resource_class = SemesterEmergencyResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

admin.site.register(SemesterEmergency, SemesterEmergencyAdmin)


class SemesterCourseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'semester_link', 'course_link', 'class_time_start',
                    'class_time_end', 'instructor_link', 'course_capacity')
    sortable_by = ('course_capacity',)
    search_fields = ('semester', 'course', 'instructor')
    search_help_text = "Search in: Semester Name, Course Name, Instructor Name"
    list_display_links = ('id', 'semester_link', 'course_link', 'instructor_link')
    resource_class = SemesterCourseResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def semester_link(self, obj):
        semester_id = obj.semester.id
        semester_url = f"http://127.0.0.1:8000/{admin_url}education/\
        semester/{semester_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           semester_url, obj.semester)
    
    def course_link(self, obj):
        course_id = obj.course.id
        course_url = f"http://127.0.0.1:8000/{admin_url}education/\
        course/{course_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           course_url, obj.course)
    
    def instructor_link(self, obj):
        instructor_id = obj.instructor.id
        instructor_url = f"http://127.0.0.1:8000/{admin_url}accounts/\
        teacher/{instructor_id}/change/"
        return format_html('<a href="{}">{}</a>',
                           instructor_url, obj.instructor)

    semester_link.short_description = "Semester"
    course_link.short_description = "Course"
    instructor_link.short_description = "Instructor"

admin.site.register(SemesterCourse, SemesterCourseAdmin)


class StudentCourseAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'student', 'get_course_name', 'status', 'score')
    list_filter = ('status',)
    sortable_by = ('score',)
    list_editable = ('status',)
    search_fields = ('student',)
    search_help_text = "Search in: Student's Username"
    resource_class = StudentCourseResource
    save_as = True
    list_per_page = 10
    list_max_show_all = 50

    def get_course_name(self, obj):
        return obj.course.course_name

    get_course_name.short_description = 'Course Name'

admin.site.register(StudentCourse, StudentCourseAdmin)

admin.site.register(Day)
