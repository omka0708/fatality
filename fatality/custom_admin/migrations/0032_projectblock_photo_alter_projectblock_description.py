# Generated by Django 5.0.2 on 2024-03-17 13:53

import custom_admin.apps
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0031_alter_projectblock_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectblock',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=custom_admin.apps.block_project_directory_path),
        ),
        migrations.AlterField(
            model_name='projectblock',
            name='description',
            field=models.CharField(max_length=2000),
        ),
    ]
