# Generated by Django 5.0 on 2024-02-23 10:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0010_responsesurvey'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_date', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnetwork.survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnetwork.question')),
                ('survey_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnetwork.surveyresponse')),
            ],
        ),
        migrations.DeleteModel(
            name='ResponseSurvey',
        ),
    ]