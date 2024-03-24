from django.contrib import admin
from dashboard_panel.models import *

admin.site.register(StudentRegistrationRequest)
admin.site.register(SemesterRegistrationRequest)
admin.site.register(AddRemoveRequest)
admin.site.register(RevisionRequest)
admin.site.register(EmergencyRemovalRequest)
admin.site.register(StudentDeleteSemesterRequest)
admin.site.register(EnrollmentRequest)