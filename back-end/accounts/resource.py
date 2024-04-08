from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from accounts.models import (User, Teacher, Student, EducationalAssistant)
from education.models import Department, Major


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'user_number',
            'national_code',
            'birthday',
            'phone',
            'address',
            'gender',
            'is_staff')
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

    class Meta:
        model = Teacher
        fields = ('id', 'user_id', 'expertise', 'rank', 'department_id', 'can_be_advisor')
        import_id_fields = ('id',)


class StudentResource(resources.ModelResource):
    user_id = fields.Field(
        column_name='user_id',
        attribute='user',
        widget=ForeignKeyWidget(User, field='id')
    )
    major_id = fields.Field(
        column_name='major_id',
        attribute='major',
        widget=ForeignKeyWidget(model=Major, field='id')
    )

    class Meta:
        model = Student
        fields = (
            'id',
            'user_id',
            'entry_year',
            'entry_semester',
            'major_id',
            'military_service_status',
            'advisor',
            'year_of_study',
            'gpa')
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

    class Meta:
        model = EducationalAssistant
        fields = ('id', 'user_id', 'field_id')
        import_id_fields = ('id',)
