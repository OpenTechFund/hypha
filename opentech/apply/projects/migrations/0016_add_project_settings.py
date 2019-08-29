# Generated by Django 2.0.13 on 2019-08-28 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('application_projects', '0015_add_payment_request_changes_requested'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compliance_email', models.TextField(verbose_name='Compliance Email')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
