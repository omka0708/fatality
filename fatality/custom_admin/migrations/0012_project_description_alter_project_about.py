# Generated by Django 5.0.2 on 2024-03-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0011_bigphotoproject_title_smallphotoproject_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='about',
            field=models.CharField(max_length=750),
        ),
    ]
