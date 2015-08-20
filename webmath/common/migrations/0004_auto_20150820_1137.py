# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20150820_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='members',
            field=models.ManyToManyField(related_name='classes', blank=True, to='common.Student'),
            preserve_default=True,
        ),
    ]
