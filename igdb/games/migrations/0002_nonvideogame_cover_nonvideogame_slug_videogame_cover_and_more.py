# Generated by Django 4.2.4 on 2024-03-25 13:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonvideogame',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='nonvideogame',
            name='slug',
            field=models.SlugField(blank=True, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='videogame',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='videogame',
            name='slug',
            field=models.SlugField(blank=True, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='nonvideogame',
            name='age_range',
            field=models.PositiveSmallIntegerField(choices=[('1+', '1+'), ('2+', '2+'), ('3+', '3+'), ('4+', '4+'), ('5+', '5+'), ('6+', '6+'), ('7+', '7+'), ('8+', '8+'), ('9+', '9+'), ('10+', '10+'), ('11+', '11+'), ('12+', '12+'), ('13+', '13+'), ('14+', '14+'), ('15+', '15+'), ('16+', '16+'), ('17+', '17+'), ('18+', '18+')]),
        ),
        migrations.AlterField(
            model_name='nonvideogame',
            name='chance',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Not applicable', 'Not applicable')], default='Not applicable'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='nonvideogame',
            name='description',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(20)]),
        ),
        migrations.AlterField(
            model_name='nonvideogame',
            name='skills',
            field=models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.MinLengthValidator(20)]),
        ),
        migrations.AlterField(
            model_name='nonvideogame',
            name='type',
            field=models.CharField(choices=[('Party Games', 'Party Games'), ('Tabletop Games', 'Tabletop Games'), ('Video Games', 'Video Games'), ('Other Games', 'Other Games')], max_length=50),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='age_range',
            field=models.PositiveSmallIntegerField(choices=[('1+', '1+'), ('2+', '2+'), ('3+', '3+'), ('4+', '4+'), ('5+', '5+'), ('6+', '6+'), ('7+', '7+'), ('8+', '8+'), ('9+', '9+'), ('10+', '10+'), ('11+', '11+'), ('12+', '12+'), ('13+', '13+'), ('14+', '14+'), ('15+', '15+'), ('16+', '16+'), ('17+', '17+'), ('18+', '18+')]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='description',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(20)]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='release_year',
            field=models.PositiveSmallIntegerField(choices=[('1958+', '1958+'), ('1959+', '1959+'), ('1960+', '1960+'), ('1961+', '1961+'), ('1962+', '1962+'), ('1963+', '1963+'), ('1964+', '1964+'), ('1965+', '1965+'), ('1966+', '1966+'), ('1967+', '1967+'), ('1968+', '1968+'), ('1969+', '1969+'), ('1970+', '1970+'), ('1971+', '1971+'), ('1972+', '1972+'), ('1973+', '1973+'), ('1974+', '1974+'), ('1975+', '1975+'), ('1976+', '1976+'), ('1977+', '1977+'), ('1978+', '1978+'), ('1979+', '1979+'), ('1980+', '1980+'), ('1981+', '1981+'), ('1982+', '1982+'), ('1983+', '1983+'), ('1984+', '1984+'), ('1985+', '1985+'), ('1986+', '1986+'), ('1987+', '1987+'), ('1988+', '1988+'), ('1989+', '1989+'), ('1990+', '1990+'), ('1991+', '1991+'), ('1992+', '1992+'), ('1993+', '1993+'), ('1994+', '1994+'), ('1995+', '1995+'), ('1996+', '1996+'), ('1997+', '1997+'), ('1998+', '1998+'), ('1999+', '1999+'), ('2000+', '2000+'), ('2001+', '2001+'), ('2002+', '2002+'), ('2003+', '2003+'), ('2004+', '2004+'), ('2005+', '2005+'), ('2006+', '2006+'), ('2007+', '2007+'), ('2008+', '2008+'), ('2009+', '2009+'), ('2010+', '2010+'), ('2011+', '2011+'), ('2012+', '2012+'), ('2013+', '2013+'), ('2014+', '2014+'), ('2015+', '2015+'), ('2016+', '2016+'), ('2017+', '2017+'), ('2018+', '2018+'), ('2019+', '2019+'), ('2020+', '2020+'), ('2021+', '2021+'), ('2022+', '2022+'), ('2023+', '2023+'), ('2024+', '2024+'), ('2025+', '2025+'), ('2026+', '2026+'), ('2027+', '2027+'), ('2028+', '2028+')], default=2006),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videogame',
            name='system_requirements',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(20)]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='type',
            field=models.CharField(choices=[('Party Games', 'Party Games'), ('Tabletop Games', 'Tabletop Games'), ('Video Games', 'Video Games'), ('Other Games', 'Other Games')], max_length=50),
        ),
    ]