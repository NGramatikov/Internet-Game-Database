# Generated by Django 4.2.4 on 2024-03-28 17:57

from django.db import migrations, models
import igdb.main.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_profile_age_profile_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthdate',
            field=models.DateTimeField(blank=True, null=True, validators=[igdb.main.validators.validate_age]),
        ),
    ]