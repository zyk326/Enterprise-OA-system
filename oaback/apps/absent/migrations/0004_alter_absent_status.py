# Generated by Django 5.0.3 on 2024-11-19 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('absent', '0003_rename_response_absent_responder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absent',
            name='status',
            field=models.IntegerField(choices=[(1, 'Auditing'), (2, 'Pass'), (3, 'Reject')], default=1),
        ),
    ]
