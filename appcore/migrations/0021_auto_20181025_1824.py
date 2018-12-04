# Generated by Django 2.0.2 on 2018-10-25 18:24

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0020_auto_20181025_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='cardsAssignee',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=None), size=None),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='cardsCreator',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=None), size=None),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]