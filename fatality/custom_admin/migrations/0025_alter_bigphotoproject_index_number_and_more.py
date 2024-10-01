# Generated by Django 5.0.2 on 2024-03-10 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0024_alter_project_index_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bigphotoproject',
            name='index_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='smallphotoproject',
            name='index_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
