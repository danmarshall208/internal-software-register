# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-04 04:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='sesa',
            field=models.CharField(default='sesa388003', max_length=20),
            preserve_default=False,
        ),
    ]