# Generated by Django 4.2.4 on 2024-03-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_nonvideogame_cover_nonvideogame_slug_videogame_cover_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonvideogame',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
