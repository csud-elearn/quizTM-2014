# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20141224_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='qcm',
            name='points',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplequestion',
            name='points',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
