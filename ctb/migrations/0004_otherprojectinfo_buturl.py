# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctb', '0003_otherprojectinfo_imgurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherprojectinfo',
            name='butUrl',
            field=models.CharField(max_length=1024, null=True),
            preserve_default=True,
        ),
    ]
