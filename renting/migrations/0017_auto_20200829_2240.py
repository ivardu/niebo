# Generated by Django 2.2 on 2020-08-29 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0016_newrentalhouse_rent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newrentalhouse',
            name='in_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='newrentalhouse',
            name='out_date',
            field=models.DateField(),
        ),
    ]