from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def year_validator(value):
    from accounts.models import Student

    if value < 1900 or value > 2100:
        raise ValidationError(
            _('Invalid year. Please enter a year between 1900 and 2100.'),
            params={'value': value},
        )
