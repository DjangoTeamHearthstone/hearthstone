# Generated by Django 2.0.2 on 2018-11-17 10:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0042_auto_20181117_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='user',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]