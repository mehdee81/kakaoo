# Generated by Django 5.0.2 on 2024-03-17 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_alter_courses_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='field',
            field=models.CharField(default='not set', max_length=200),
        ),
    ]
