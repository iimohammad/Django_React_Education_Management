from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from education.models import Department, Course, Semester, Major


class DepartmentResource(resources.ModelResource):
     class Meta:
         model = Department
         fields = ('id', 'department_name', 'department_code', 'year_established',
                   'department_location', 'number_of_students')
         import_id_fields = ('id',)


class MajorResource(resources.ModelResource):
    department_id = fields.Field(
        column_name='department_id',
        attribute='department',
        widget=ForeignKeyWidget(Department, field='id')
    )

    class Meta:
        model = Major
        fields = ('id', 'major_name', 'major_code', 'department_id', 'number_of_credits',
                  'level', 'education_group')
        import_id_fields = ('id',)


class CourseResource(resources.ModelResource):
     class Meta:
         model = Course
         fields = ('id', 'course_name', 'course_code', 'credit_num')
         import_id_fields = ('id',)


class SemesterResource(resources.ModelResource):
     class Meta:
         model = Semester
         fields = ('id', 'name', 'selection_start', 'selection_end', 'start_semester',
                   'end_semester', 'exam_start', 'exam_end', 'add_remove_start', 'add_remove_end',
                   'emergency_remove_start', 'emergency_remove_end', 'classes_start', 'classes_end')
         import_id_fields = ('id',)
