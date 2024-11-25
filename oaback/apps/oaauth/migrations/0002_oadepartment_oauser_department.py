# Generated by Django 5.0.3 on 2024-11-18 10:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oaauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OADepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('intro', models.CharField(max_length=200)),
                ('leader', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader_department', related_query_name='leader_department', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_department', related_query_name='manager_department', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='oauser',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs', related_query_name='staff', to='oaauth.oadepartment'),
        ),
    ]
