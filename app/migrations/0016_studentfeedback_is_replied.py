# Generated by Django 5.1.3 on 2024-12-13 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_stafffeedback_feedback_replay_studentfeedback_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentfeedback',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
    ]
