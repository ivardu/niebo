# Generated by Django 2.2 on 2020-08-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0015_auto_20200825_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='newrentalhouse',
            name='rent',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
