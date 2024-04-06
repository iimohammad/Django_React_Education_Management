from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, user_number, password=None, **extra_fields):
        """
        Create and return a regular user with the given user_number and password.
        """
        if not user_number:
            raise ValueError('The user number must be set')
        user = self.model(user_number=user_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_number, password=None, **extra_fields):
        """
        Create and return a superuser with the given user_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_number, password, **extra_fields)
