# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dotask',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='incomeMoney',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='outPutMoney',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
