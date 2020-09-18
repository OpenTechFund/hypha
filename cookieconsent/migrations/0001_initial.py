# Generated by Django 2.2.16 on 2020-09-18 08:53

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookieConsentSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookieconsent_active', models.BooleanField(default=False, verbose_name='Activate cookie concent feature')),
                ('cookieconsent_title', models.CharField(default='Your cookie settings', max_length=255)),
                ('cookieconsent_message', wagtail.core.fields.RichTextField(default='This website deploys cookies for basic functionality and to keep it secure. These cookies are strictly necessary. Optional analysis cookies which provide us with statistical information about the use of the website may also be deployed, but only with your consent. Please review our <a href="/data-privacy-policy/">Privacy & Data Policy</a> for more information.')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Cookie consent settings',
            },
        ),
    ]
