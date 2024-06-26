# Generated by Django 4.2.4 on 2024-03-30 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_alter_nonvideogame_age_range_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonvideogame',
            name='type',
            field=models.CharField(choices=[('Party Games', 'Party Games'), ('Tabletop Games', 'Tabletop Games'), ('Video Games', 'Video Games'), ('Other Games', 'Other Games')], default='Video Games', max_length=50),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='type',
            field=models.CharField(choices=[('Party Games', 'Party Games'), ('Tabletop Games', 'Tabletop Games'), ('Video Games', 'Video Games'), ('Other Games', 'Other Games')], default='Video Games', max_length=50),
        ),
    ]
