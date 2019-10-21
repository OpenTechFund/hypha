# Generated by Django 2.0.10 on 2019-02-07 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('funds', '0052_reviewerrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedReviewers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer', models.ForeignKey(limit_choices_to={'groups__name__in': ['Staff', 'Reviewer']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='funds.ReviewerRole')),
            ],
        ),
        migrations.AlterField(
            model_name='applicationsubmission',
            name='reviewers',
            field=models.ManyToManyField(blank=True, limit_choices_to={'groups__name__in': ['Staff', 'Reviewer']}, related_name='submissions_reviewer_OLD', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignedreviewers',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to='funds.ApplicationSubmission'),
        ),
        migrations.AddField(
            model_name='applicationsubmission',
            name='reviewers_new',
            field=models.ManyToManyField(blank=True, related_name='submissions_reviewer', through='funds.AssignedReviewers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='assignedreviewers',
            unique_together={('submission', 'role')},
        ),
    ]
