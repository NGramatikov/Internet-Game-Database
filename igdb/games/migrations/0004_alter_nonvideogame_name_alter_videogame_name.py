# Generated by Django 4.2.4 on 2024-03-25 16:32

from django.db import migrations, models
import igdb.games.validators


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_alter_nonvideogame_slug_alter_videogame_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonvideogame',
            name='name',
            field=models.CharField(max_length=100, unique=True, validators=[igdb.games.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='name',
            field=models.CharField(max_length=100, unique=True, validators=[igdb.games.validators.validate_name]),
        ),
    ]