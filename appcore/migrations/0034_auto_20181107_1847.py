# Generated by Django 2.0.2 on 2018-11-07 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appcore', '0033_deck_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchange',
            old_name='cardsAssignee',
            new_name='cards_assignee',
        ),
        migrations.RenameField(
            model_name='exchange',
            old_name='cardsCreator',
            new_name='cards_creator',
        ),
    ]
