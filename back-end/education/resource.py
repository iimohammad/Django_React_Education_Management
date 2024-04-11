from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from accounts.models import Teacher, Student
from education.models import (Course,
                              Department,
                              Major,
                              Day,
                              Semester,
                              SemesterUnitSelection,
                              SemesterClass,
                              SemesterAddRemove,
                              SemesterExam,
                              SemesterEmergency,
                              Prerequisite,
                              Requisite,
                              SemesterCourse,
                              StudentCourse)


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = (
            'id',
            'department_name',
            'department_code',
            'year_established',
            'department_location')
        import_id_fields = ('id',)


class MajorResource(resources.ModelResource):
    department_id = fields.Field(
        column_name='department_id',
        attribute='department',
        widget=ForeignKeyWidget(Department, field='id')
    )

    class Meta:
        model = Major
        fields = (
            'id',
            'major_name',
            'major_code',
            'department_id',
            'number_of_credits',
            'level',
            'education_group')
        import_id_fields = ('id',)


class CourseResource(resources.ModelResource):
    department_id = fields.Field(
        column_name='department_id',
        attribute='department',
        widget=ForeignKeyWidget(Department, field='id')
    )
    major_id = fields.Field(
        column_name='major_id',
        attribute='major',
        widget=ForeignKeyWidget(Major, field='id')
    )

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_code', 'credit_num', 'department_id',
                  'major_id', 'course_type', 'availablity')
        import_id_fields = ('id',)


class SemesterResource(resources.ModelResource):
    class Meta:
        model = Semester
        fields = ('id', 'name', 'start_semester',
                  'end_semester', 'semester_type')
        import_id_fields = ('id',)


class SemesterUnitSelectionResource(resources.ModelResource):
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )

    class Meta:
        model = SemesterUnitSelection
        fields = ('id', 'semester_id', 'unit_selection_start',
                  'unit_selection_end')
        import_id_fields = ('id',)


class SemesterClassResource(resources.ModelResource):
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )

    class Meta:
        model = SemesterClass
        fields = ('id', 'semester_id', 'classes_start',
                  'classes_end')
        import_id_fields = ('id',)


class SemesterAddRemoveResource(resources.ModelResource):
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )

    class Meta:
        model = SemesterAddRemove
        fields = ('id', 'semester_id', 'addremove_start',
                  'addremove_end')
        import_id_fields = ('id',)


class SemesterExamResource(resources.ModelResource):
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )

    class Meta:
        model = SemesterExam
        fields = ('id', 'semester_id', 'exam_start',
                  'exam_end')
        import_id_fields = ('id',)


class SemesterEmergencyResource(resources.ModelResource):
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )

    class Meta:
        model = SemesterEmergency
        fields = ('id', 'semester_id', 'emergency_remove_start',
                  'emergency_remove_end')
        import_id_fields = ('id',)


class PrerequisiteResource(resources.ModelResource):
    course_id = fields.Field(
        column_name='course_id',
        attribute='course',
        widget=ForeignKeyWidget(Course, field='id')
    )
    prerequisite_id = fields.Field(
        column_name='prerequisite_id',
        attribute='prerequisite',
        widget=ForeignKeyWidget(Course, field='id')
    )

    class Meta:
        model = Prerequisite
        fields = ('id', 'course_id', 'prerequisite_id')
        import_id_fields = ('id',)


class RequisiteResource(resources.ModelResource):
    course_id = fields.Field(
        column_name='course_id',
        attribute='course',
        widget=ForeignKeyWidget(Course, field='id')
    )
    requisite_id = fields.Field(
        column_name='requisite_id',
        attribute='requisite',
        widget=ForeignKeyWidget(Course, field='id')
    )

    class Meta:
        model = Requisite
        fields = ('id', 'course_id', 'requisite_id')
        import_id_fields = ('id',)


class SemesterCourseResource(resources.ModelResource):
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )
    course_id = fields.Field(
        column_name='course_id',
        attribute='course',
        widget=ForeignKeyWidget(Course, field='id')
    )
    class_days_ids = fields.Field(
        column_name='class_days_ids',
        attribute='class_days',
        widget=ManyToManyWidget(Day, field='id')
    )
    instructor_id = fields.Field(
        column_name='instructor_id',
        attribute='instructor',
        widget=ForeignKeyWidget(Teacher, field='id')
    )

    class Meta:
        model = SemesterCourse
        fields = ('id', 'semester_id', 'course_id', 'class_days_ids',
                  'class_time_start', 'class_time_end', 'exam_datetime',
                  'exam_location', 'instructor_id', 'course_capacity',
                  'corse_reserve_capasity')
        import_id_fields = ('id',)


class StudentCourseResource(resources.ModelResource):
    student_id = fields.Field(
        column_name='student_id',
        attribute='student',
        widget=ForeignKeyWidget(Student, field='id')
    )
    semester_course_id = fields.Field(
        column_name='semester_course_id',
        attribute='semester_course',
        widget=ForeignKeyWidget(SemesterCourse, field='id')
    )

    class Meta:
        model = StudentCourse
        fields = ('id', 'student_id', 'semester_course_id', 'status', 'score')
        import_id_fields = ('id',)
