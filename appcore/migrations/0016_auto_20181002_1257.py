# Generated by Django 2.0.2 on 2018-10-02 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0015_auto_20181002_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]