# Generated by Django 2.0.2 on 2018-08-29 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_customimage_file_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='customimage',
            name='drupal_id',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]