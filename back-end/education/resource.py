from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from education.models import Course, Department, Major, Semester


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
    prerequisite_id = fields.Field(
        column_name='prerequisite_id',
        attribute='prerequisite',
        widget=ForeignKeyWidget(Course, field='id')
    )
    corequisite_id = fields.Field(
        column_name='corequisite_id',
        attribute='corequisite',
        widget=ForeignKeyWidget(Course, field='id')
    )

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'course_code', 'credit_num',
                  'prerequisite_id', 'corequisite_id')
        import_id_fields = ('id',)


class SemesterResource(resources.ModelResource):
    class Meta:
        model = Semester
        fields = ('id', 'name', 'start_semester',
                  'end_semester', 'semester_type')
        import_id_fields = ('id',)
