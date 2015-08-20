# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20150820_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='owner',
            field=models.ForeignKey(related_name='classes', to='common.Teacher'),
            preserve_default=True,
        ),
    ]
