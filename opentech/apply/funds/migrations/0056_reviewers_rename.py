# Generated by Django 2.0.10 on 2019-02-07 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0055_remove_applicationsubmission_reviewers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationsubmission',
            old_name='reviewers_new',
            new_name='reviewers',
        ),
    ]
