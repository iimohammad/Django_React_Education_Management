from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class SetAccessRestrictions(BaseCommand):
    help = 'Description of your custom command'

    def handle(self, *args, **options):
        educational_assistants_group, created = Group.objects.get_or_create(
            name="Educational Assistants")

        # Assign specific permissions to the group
        # Example: Allow view and change permissions for the Transaction model
        educational_assistants_permissions = Permission.objects.filter(
            content_type__app_label="admin_dashboard_panel",
            codename__in=["view_transaction", "change_transaction"],
        )
        educational_assistants_group.permissions.set(
            educational_assistants_permissions)

        self.stdout.write(
            'Access restrictions for educational assisstants are applied successfully.')
