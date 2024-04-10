# Generated by Django 4.2.4 on 2024-04-10 05:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import igdb.main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('birthdate', models.DateField(blank=True, null=True, validators=[igdb.main.validators.validate_age])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
