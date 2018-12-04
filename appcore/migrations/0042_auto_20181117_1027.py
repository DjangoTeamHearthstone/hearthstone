# Generated by Django 2.0.2 on 2018-11-17 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0041_deck_official'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deck',
            name='cards',
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ManyToManyField(default=None, to='appcore.Deck'),
        ),
    ]