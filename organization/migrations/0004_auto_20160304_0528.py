# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20160304_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultyverification',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='studentleaderverification',
            name='is_verified',
        ),
        migrations.AddField(
            model_name='facultyverification',
            name='citation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facultyverification',
            name='verification_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Verified'), (2, 'Rejected')], default=0),
        ),
        migrations.AddField(
            model_name='studentleaderverification',
            name='citation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentleaderverification',
            name='verification_status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Verified'), (2, 'Rejected')], default=0),
        ),
    ]