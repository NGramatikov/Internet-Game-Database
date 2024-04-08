from datetime import datetime
from django.core.exceptions import ValidationError

"""
The difference between two datetime objects returns a timedelta object which does not have years so we have to check
if the person has had their birthday yet this year.
"""


def validate_age(birthday):
    today = datetime.now()
    age = today.year - birthday.year

    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1

    if age <= 12:
        raise ValidationError("You must be at least 12 years old.")
