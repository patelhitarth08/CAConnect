# Generated by Django 4.1.7 on 2023-06-14 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAadmin', '0006_client_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Admin', 'Admin'), ('Employee', 'Client'), ('Client', 'Client')], max_length=10)),
            ],
        ),
    ]
