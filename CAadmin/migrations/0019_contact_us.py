# Generated by Django 4.1.7 on 2023-06-28 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAadmin', '0018_alter_ca_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=255)),
                ('messaeg', models.CharField(max_length=255)),
                ('ref', models.CharField(max_length=255)),
            ],
        ),
    ]
