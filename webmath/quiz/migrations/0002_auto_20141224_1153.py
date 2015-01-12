# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qcmsubmitone',
            name='id_selected',
            field=models.ForeignKey(blank=True, to='quiz.QcmChoice'),
            preserve_default=True,
        ),
    ]
