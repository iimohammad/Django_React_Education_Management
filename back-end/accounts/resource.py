from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from accounts.models import User, Teacher
from education.models import Department, Course, Semester, Major


class UserResource(resources.ModelResource):
     class Meta:
         model = User
         fields = ('id', 'username', 'password', 'first_name', 'last_name', 'user_number',
                   'national_code', 'birthday', 'phone', 'address', 'gender')
         import_id_fields = ('id',)


class TeacherResource(resources.ModelResource):
    user_id = fields.Field(
        column_name='user_id',
        attribute='user',
        widget=ForeignKeyWidget(User, field='id')
    )
    department_id = fields.Field(
        column_name='department_id',
        attribute='department',
        widget=ForeignKeyWidget(Department, field='id')
    )
    past_courses_id = fields.Field(
        column_name='past_courses_id',
        attribute='past_courses',
        widget=ForeignKeyWidget(model=Course, field='id')
    )

    class Meta:
        model = Teacher
        fields = ('id', 'user_id', 'expertise', 'rank',
                  'department_id', 'past_courses_id')
        import_id_fields = ('id',)


class StudentResource(resources.ModelResource):
    user_id = fields.Field(
        column_name='user_id',
        attribute='user',
        widget=ForeignKeyWidget(User, field='id')
    )
    entry_semester_id = fields.Field(
        column_name='entry_semester_id',
        attribute='entry_semester',
        widget=ForeignKeyWidget(model=Semester, field='id')
    )
    major_id = fields.Field(
        column_name='major_id',
        attribute='major',
        widget=ForeignKeyWidget(model=Major, field='id')
    )

    class Meta:
        model = Teacher
        fields = ('id', 'user_id', 'entry_year', 'entry_semester_id',
                  'major_id', 'military_service_status', 'year_of_study', 'gpa')
        import_id_fields = ('id',)


class EducationalAssistantResource(resources.ModelResource):
    user_id = fields.Field(
        column_name='user_id',
        attribute='user',
        widget=ForeignKeyWidget(model=User, field='id')
    )
    field_id = fields.Field(
        column_name='field_id',
        attribute='field',
        widget=ForeignKeyWidget(model=Major, field='id')
    )
    department_id = fields.Field(
        column_name='department_id',
        attribute='department',
        widget=ForeignKeyWidget(model=Department, field='id')
    )

    class Meta:
        model = Teacher
        fields = ('id', 'user_id', 'field_id', 'department_id')
        import_id_fields = ('id',)
