# Generated by Django 5.1.3 on 2024-12-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_staffnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffnotification',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]