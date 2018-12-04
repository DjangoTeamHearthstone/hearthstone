# Generated by Django 2.0.2 on 2018-10-28 15:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0029_auto_20181028_1041'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardOrigins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('cost', models.IntegerField(null=True)),
                ('health', models.IntegerField(null=True)),
                ('attack', models.IntegerField(null=True)),
                ('text', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeckOrigins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cards', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=None), size=None)),
                ('cost', models.IntegerField(null=True)),
            ],
        ),
    ]
