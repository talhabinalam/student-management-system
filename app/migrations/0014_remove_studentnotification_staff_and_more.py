# Generated by Django 5.1.3 on 2024-12-12 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_customuser_user_type_studentnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentnotification',
            name='staff',
        ),
        migrations.AddField(
            model_name='studentnotification',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.student'),
            preserve_default=False,
        ),
    ]