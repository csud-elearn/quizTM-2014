# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('quiz', '0003_quiz_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizdraft',
            name='id_teacher',
            field=models.ForeignKey(default=0, to='common.Teacher'),
            preserve_default=False,
        ),
    ]
