# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='checkRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userId', models.IntegerField(default=0, db_index=True)),
                ('businessId', models.IntegerField(default=0, db_index=True)),
                ('type', models.IntegerField(default=0)),
                ('isDone', models.BigIntegerField(default=0)),
                ('createTime', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='incomestream',
            old_name='getTask',
            new_name='getTaskId',
        ),
        migrations.RenameField(
            model_name='outstream',
            old_name='getTask',
            new_name='getTaskId',
        ),
        migrations.RenameField(
            model_name='taskstream',
            old_name='getTask',
            new_name='getTaskId',
        ),
        migrations.AddField(
            model_name='carinfo',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='openId',
            field=models.CharField(unique=True, max_length=64),
        ),
    ]
