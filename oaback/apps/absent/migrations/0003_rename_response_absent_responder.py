# Generated by Django 5.0.3 on 2024-11-19 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('absent', '0002_alter_absent_response_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='absent',
            old_name='response',
            new_name='responder',
        ),
    ]
