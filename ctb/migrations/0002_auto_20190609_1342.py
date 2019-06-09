# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherprojectinfo',
            name='configFrame',
            field=models.CharField(max_length=512, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='otherprojectinfo',
            name='configUrl',
            field=models.CharField(max_length=1024, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='otherprojectinfo',
            name='developer',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='otherautohandshakeuser',
            name='clientUUId',
            field=models.CharField(max_length=255, db_index=True),
        ),
    ]
