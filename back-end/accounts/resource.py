from import_export import resources, fields
from .models import User, Student, Teacher, EducationalAssistant

class UserResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID', readonly=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_number', 'national_code', 'birthday', 'phone', 'address', 'gender']
        import_id_fields = ['id']

    def before_import_row(self, row, **kwargs):
        if 'id' not in row:
            row['id'] = None

class TeacherResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID', readonly=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user__username', 'expertise', 'rank', 'department__department_name']
        import_id_fields = ['id']

    def before_import_row(self, row, **kwargs):
        if 'id' not in row:
            row['id'] = None

class StudentResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID', readonly=True)

    class Meta:
        model = Student
        fields = ['id', 'user__username', 'entry_semester', 'gpa', 'entry_year', 'major__major_name', 'advisor__user__username', 'military_service_status', 'year_of_study']
        import_id_fields = ['id']

    def before_import_row(self, row, **kwargs):
        if 'id' not in row:
            row['id'] = None

class EducationalAssistantResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='ID', readonly=True)

    class Meta:
        model = EducationalAssistant
        fields = ['id', 'user__username', 'field__major_name']
        import_id_fields = ['id']

    def before_import_row(self, row, **kwargs):
        if 'id' not in row:
            row['id'] = None
