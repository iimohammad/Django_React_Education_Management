from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from dashboard_student.models import (SemesterRegistrationRequest,
                                      UnitSelectionRequest,
                                      AddRemoveRequest,
                                      RevisionRequest,
                                      EmergencyRemovalRequest,
                                      StudentDeleteSemesterRequest,
                                      EmploymentEducationRequest)
from accounts.models import Student, Teacher
from education.models import (Semester,
                              Course,
                              SemesterCourse,
                              StudentCourse)


class SemesterRegistrationRequestResource(resources.ModelResource):
    student_id = fields.Field(
        column_name='student_id',
        attribute='student',
        widget=ForeignKeyWidget(Student, field='id')
    )
    semester_id = fields.Field(
        column_name='semester_id',
        attribute='semester',
        widget=ForeignKeyWidget(Semester, field='id')
    )
    course_ids = fields.Field(
        column_name='course_ids',
        attribute='requested_courses',
        widget=ManyToManyWidget(Course, field='id')
    )

    class Meta:
        model = SemesterRegistrationRequest
        fields = ('id', 'student_id', 'semester_id', 'approval_status',
                  'created_at', 'course_ids', 'teacher_comment_for_requested_courses')
        import_id_fields = ('id',)


class UnitSelectionRequestResource(resources.ModelResource):
    semester_registration_request_id = fields.Field(
        column_name='semester_registration_request_id',
        attribute='semester_registration_request',
        widget=ForeignKeyWidget(SemesterRegistrationRequest, field='id')
    )
    semester_course_ids = fields.Field(
        column_name='semester_course_ids',
        attribute='requested_courses',
        widget=ManyToManyWidget(SemesterCourse, field='id')
    )

    class Meta:
        model = UnitSelectionRequest
        fields = ('id', 'semester_registration_request_id', 'approval_status',
                  'created_at', 'semester_course_ids')
        import_id_fields = ('id',)


class AddRemoveRequestResource(resources.ModelResource):
    semester_registration_request_id = fields.Field(
        column_name='semester_registration_request_id',
        attribute='semester_registration_request',
        widget=ForeignKeyWidget(SemesterRegistrationRequest, field='id')
    )
    removed_courses_ids = fields.Field(
        column_name='removed_courses_ids',
        attribute='removed_courses',
        widget=ManyToManyWidget(StudentCourse, field='id')
    )
    added_courses_ids = fields.Field(
        column_name='added_courses_ids',
        attribute='added_courses',
        widget=ManyToManyWidget(StudentCourse, field='id')
    )

    class Meta:
        model = AddRemoveRequest
        fields = ('id', 'semester_registration_request_id', 'approval_status',
                  'created_at', 'removed_courses_ids', 'added_courses_ids')
        import_id_fields = ('id',)


class RevisionRequestResource(resources.ModelResource):
    student_id = fields.Field(
        column_name='student_id',
        attribute='student',
        widget=ForeignKeyWidget(Student, field='id')
    )
    student_course_id = fields.Field(
        column_name='student_course_id',
        attribute='course',
        widget=ForeignKeyWidget(StudentCourse, field='id')
    )

    class Meta:
        model = RevisionRequest
        fields = ('id', 'student_id', 'teacher_approval_status',
                 'educational_assistant_approval_status', 'created_at',
                 'student_course_id', 'text', 'answer')
        import_id_fields = ('id',)


class EmergencyRemovalRequestResource(resources.ModelResource):
    student_id = fields.Field(
        column_name='student_id',
        attribute='student',
        widget=ForeignKeyWidget(Student, field='id')
    )
    student_course_id = fields.Field(
        column_name='student_course_id',
        attribute='course',
        widget=ForeignKeyWidget(StudentCourse, field='id')
    )

    class Meta:
        model = EmergencyRemovalRequest
        fields = ('id', 'student_id', 'approval_status', 'created_at',
                  'student_course_id', 'student_explanation', 'educational_assistant_explanation')
        import_id_fields = ('id',)


class StudentDeleteSemesterRequestResource(resources.ModelResource):
    semester_registration_request_id = fields.Field(
        column_name='semester_registration_request_id',
        attribute='semester_registration_request',
        widget=ForeignKeyWidget(SemesterRegistrationRequest, field='id')
    )

    class Meta:
        model = StudentDeleteSemesterRequest
        fields = ('id', 'semester_registration_request_id', 'teacher_approval_status',
                  'educational_assistant_approval_status', 'created_at',
                  'student_explanations', 'educational_assistant_explanation')
        import_id_fields = ('id',)



class EmploymentEducationRequestResource(resources.ModelResource):
    student_id = fields.Field(
        column_name='student_id',
        attribute='student',
        widget=ForeignKeyWidget(Student, field='id')
    )

    class Meta:
        model = EmploymentEducationRequest
        fields = ('id', 'student_id', 'approval_status', 'created_at', 'need_for')
        import_id_fields = ('id',)
