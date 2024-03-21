from django.db import models
from accounts.models import User


class Admin(User):
    user_number = models.CharField(max_length=255, null=True)
    national_code = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
