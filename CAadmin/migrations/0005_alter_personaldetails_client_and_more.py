# Generated by Django 4.1.7 on 2023-06-10 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CAadmin', '0004_alter_ca_username_alter_client_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaldetails',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CAadmin.client'),
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
