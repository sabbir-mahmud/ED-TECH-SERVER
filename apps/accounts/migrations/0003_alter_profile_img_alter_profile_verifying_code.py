# Generated by Django 4.1.1 on 2022-09-07 04:55

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_verified_profile_verifying_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=apps.accounts.models.img_uploader),
        ),
        migrations.AlterField(
            model_name='profile',
            name='verifying_code',
            field=models.CharField(max_length=6),
        ),
    ]
