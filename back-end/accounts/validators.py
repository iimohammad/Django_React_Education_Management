from django.core import validators
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r'^09\d{9}$'
    message = (
        'Enter a valid mobile number. This value may contain numbers only, '
        'and must be exactly 11 digits starting with "09"'
    )
    flags = 0


phone_validator = PhoneValidator()


def validate_national_code(value):
    if not value.isdigit():
        raise ValidationError('National code must contain only digits.')
    if len(value) != 10:
        raise ValidationError('National code must be 10 digits long.')