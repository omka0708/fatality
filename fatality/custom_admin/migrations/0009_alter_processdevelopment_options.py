# Generated by Django 5.0.2 on 2024-03-02 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0008_alter_processdevelopment_index_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processdevelopment',
            options={'ordering': ['id', 'index_number']},
        ),
    ]
