# Generated by Django 2.2 on 2020-07-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0008_auto_20200707_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newrentalhouse',
            name='house_no',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='newrentalhouse',
            name='zipcode',
            field=models.CharField(max_length=12),
        ),
    ]
