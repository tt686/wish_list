# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-31 05:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0002_auto_20180129_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='playlists',
            field=models.ManyToManyField(related_name='favorite_songs', to='login_registration_app.User'),
        ),
    ]
