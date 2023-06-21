# Generated by Django 4.1.7 on 2023-06-21 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CAadmin', '0009_employee_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personal_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=20)),
                ('month', models.CharField(max_length=15)),
                ('year', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=20)),
                ('file', models.FileField(upload_to='media/personal_files')),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='CAadmin.client')),
            ],
        ),
        migrations.CreateModel(
            name='General_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='media/general_files')),
                ('client', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='CAadmin.client')),
            ],
        ),
    ]
