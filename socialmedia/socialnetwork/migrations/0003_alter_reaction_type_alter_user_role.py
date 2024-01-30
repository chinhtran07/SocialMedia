# Generated by Django 5.0 on 2024-01-29 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_question_alumniprofile_friendship_group_invitation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='type',
            field=models.IntegerField(choices=[(1, 'Like'), (2, 'Haha'), (3, 'Love')], null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'Lecturer'), (3, 'Admin')], default=1),
        ),
    ]
