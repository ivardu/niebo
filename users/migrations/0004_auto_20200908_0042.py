# Generated by Django 2.2 on 2020-09-07 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200825_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
