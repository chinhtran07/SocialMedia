# Generated by Django 5.0 on 2024-02-23 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0007_alter_choice_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='place',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]