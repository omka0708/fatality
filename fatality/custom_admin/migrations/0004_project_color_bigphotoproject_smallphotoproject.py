# Generated by Django 5.0.2 on 2024-03-02 18:54

import custom_admin.apps
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0003_alter_review_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='color',
            field=models.CharField(default='#ABCDEF', max_length=7, validators=[django.core.validators.RegexValidator(message='Введите код цвета', regex='^#(?:[0-9a-fA-F]{3}){1,2}$')]),
        ),
        migrations.CreateModel(
            name='BigPhotoProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(upload_to=custom_admin.apps.big_photo_project_directory_path)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='big_photos', to='custom_admin.project')),
            ],
        ),
        migrations.CreateModel(
            name='SmallPhotoProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(upload_to=custom_admin.apps.small_photo_project_directory_path)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='small_photos', to='custom_admin.project')),
            ],
        ),
    ]
