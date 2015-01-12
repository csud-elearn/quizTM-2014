# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20141231_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qcm',
            name='points',
            field=models.FloatField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simplequestion',
            name='points',
            field=models.FloatField(default=1),
            preserve_default=True,
        ),
    ]
