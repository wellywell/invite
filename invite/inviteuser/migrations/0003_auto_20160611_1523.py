# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-06-11 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inviteuser', '0002_auto_20160611_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inviteduser',
            name='invite',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inviteuser.Invite'),
        ),
    ]