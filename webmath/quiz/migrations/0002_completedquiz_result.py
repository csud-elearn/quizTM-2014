# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedquiz',
            name='result',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
