# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outstream',
            old_name='getTaskId',
            new_name='checkRecordId',
        ),
        migrations.RemoveField(
            model_name='gettask',
            name='startdoTaskTime',
        ),
        migrations.AddField(
            model_name='incomestream',
            name='checkRecordId',
            field=models.IntegerField(default=0, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incomestream',
            name='endTime',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='incomestream',
            name='status',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
    ]
