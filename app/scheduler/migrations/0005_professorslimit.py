# Generated by Django 5.0.2 on 2024-03-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_rename_c_to_p_ctop'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessorsLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Professor', models.CharField(max_length=200)),
                ('day', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=200)),
            ],
        ),
    ]