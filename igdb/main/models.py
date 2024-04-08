from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from igdb.main.validators import validate_age

# Create your models here.
user = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=user,
        on_delete=models.CASCADE,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    avatar = models.ImageField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    country = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    birthdate = models.DateField(
        null=True,
        blank=True,
        validators=[
            validate_age,
        ],
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
