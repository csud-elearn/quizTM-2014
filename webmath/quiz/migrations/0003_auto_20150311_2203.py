# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20150311_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='qcmsubmitmulti',
            name='result',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='qcmsubmitone',
            name='result',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sqsubmit',
            name='result',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
