# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_completedquiz_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='points',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
