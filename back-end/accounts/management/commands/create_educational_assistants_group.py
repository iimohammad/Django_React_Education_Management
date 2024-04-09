from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from accounts.models import EducationalAssistant


# create_educational_assistants_group
class Command(BaseCommand):
    help = "Creates an 'Educational Assistants' group and assigns permissions."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Educational Assistants')

        permissions = [
            Permission.objects.get(codename='add_course'),
            Permission.objects.get(codename='view_course'),
            Permission.objects.get(codename='change_course'),
            Permission.objects.get(codename='delete_course'),
            Permission.objects.get(codename='add_semestercourse'),
            Permission.objects.get(codename='view_semestercourse'),
            Permission.objects.get(codename='change_semestercourse'),
            Permission.objects.get(codename='delete_semestercourse'),
            Permission.objects.get(codename='view_teacher'),
            Permission.objects.get(codename='view_student'),
            Permission.objects.get(codename='view_revisionrequest'),
            Permission.objects.get(codename='change_revisionrequest'),
            Permission.objects.get(codename='view_emergencyremovalrequest'),
            Permission.objects.get(codename='change_emergencyremovalrequest'),
            Permission.objects.get(codename='view_enrollmentrequest'),
            Permission.objects.get(codename='change_enrollmentrequest'),
            Permission.objects.get(codename='view_employmenteducationrequest'),
            Permission.objects.get(codename='change_employmenteducationrequest'),
            Permission.objects.get(codename='view_studentdeletesemesterrequest'),
            Permission.objects.get(codename='change_studentdeletesemesterrequest'),
        ]
        group.permissions.add(*permissions)

        educational_assistants = EducationalAssistant.objects.all()
        for ea in educational_assistants:
            ea.user.groups.add(group)

        self.stdout.write(self.style.SUCCESS("Educational \
                            Assistants group created and permissions assigned."))
