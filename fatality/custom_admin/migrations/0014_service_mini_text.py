# Generated by Django 5.0.2 on 2024-03-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0013_alter_processdevelopment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='mini_text',
            field=models.CharField(default='', max_length=500),
        ),
    ]
