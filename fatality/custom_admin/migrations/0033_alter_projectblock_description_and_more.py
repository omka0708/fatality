# Generated by Django 5.0.2 on 2024-03-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0032_projectblock_photo_alter_projectblock_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectblock',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='projectblock',
            name='title',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
