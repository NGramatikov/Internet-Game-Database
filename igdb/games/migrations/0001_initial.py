# Generated by Django 4.2.4 on 2024-04-10 05:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import igdb.games.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, validators=[igdb.games.validators.validate_name])),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(20)])),
                ('type', models.CharField(choices=[('Party Games', 'Party Games'), ('Tabletop Games', 'Tabletop Games'), ('Video Games', 'Video Games'), ('Other Games', 'Other Games')], default='Video Games', max_length=50)),
                ('genre', models.CharField(blank=True, max_length=50, null=True)),
                ('age_range', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18)])),
                ('cover', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('release_year', models.PositiveSmallIntegerField(choices=[(1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028)])),
                ('trailer', models.URLField(blank=True, null=True)),
                ('gameplay', models.URLField(blank=True, null=True)),
                ('developer', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('system_requirements', models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(20)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NonVideoGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, validators=[igdb.games.validators.validate_name])),
                ('description', models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(20)])),
                ('type', models.CharField(choices=[('Party Games', 'Party Games'), ('Tabletop Games', 'Tabletop Games'), ('Video Games', 'Video Games'), ('Other Games', 'Other Games')], default='Video Games', max_length=50)),
                ('genre', models.CharField(blank=True, max_length=50, null=True)),
                ('age_range', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18)])),
                ('cover', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('players', models.PositiveSmallIntegerField()),
                ('rules', models.TextField()),
                ('setup_time', models.TimeField(blank=True, null=True)),
                ('playtime', models.TimeField(blank=True, null=True)),
                ('chance', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Not applicable', 'Not applicable')])),
                ('skills', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.MinLengthValidator(20)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
