
# Generated by Django 2.0.9 on 2018-12-19 13:21
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations

from opentech.apply.users.groups import GROUPS, TEAMADMIN_GROUP_NAME, PARTNER_GROUP_NAME


def add_groups(apps, schema_editor):
    # Workaround for https://code.djangoproject.com/ticket/23422
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, db_alias)

    Group = apps.get_model('auth.Group')
    Permission = apps.get_model('auth.Permission')

    for group_data in GROUPS:
        group, created = Group.objects.get_or_create(name=group_data['name'])
        for permission in group_data['permissions']:
            try:
                group.permissions.add(Permission.objects.get(codename=permission))
            except ObjectDoesNotExist:
                print("Could not find the '%s' permission" % permission)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth.Group')
    Group.objects.filter(name__in=[TEAMADMIN_GROUP_NAME, PARTNER_GROUP_NAME]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_add_staff_permissions'),
    ]

    operations = [
        migrations.RunPython(add_groups, remove_groups)
    ]
