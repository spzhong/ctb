# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0002_auto_20190131_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=520, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='trueName',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
