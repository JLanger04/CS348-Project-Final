# Generated by Django 5.0.1 on 2024-04-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_movies_duration_alter_movies_release_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='release_year',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='ranked',
            name='rating',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
