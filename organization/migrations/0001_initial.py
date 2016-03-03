# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-03 19:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('student_leader_username', models.CharField(max_length=64)),
                ('faculty_in_charge_username', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of post', max_length=64)),
                ('is_post', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_and_rewards', to='organization.Organization')),
            ],
            options={
                'verbose_name_plural': 'Posts and Awards',
                'verbose_name': 'Posts and Awards',
            },
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('is_verified_by_student_leader', models.BooleanField(default=False)),
                ('is_verified_by_faculty', models.BooleanField(default=False)),
                ('verified_by_student_leader_at', models.DateTimeField(editable=False, null=True)),
                ('verified_by_faculty_at', models.DateTimeField(editable=False, null=True)),
                ('organization_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipients', to='organization.OrganizationObject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
