# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quizdraft_id_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qcm',
            name='show_list',
        ),
        migrations.AlterField(
            model_name='qcm',
            name='multi_answers',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
