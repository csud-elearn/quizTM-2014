# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20141231_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qcmsubmitmulti',
            name='id_selected',
            field=models.ManyToManyField(null=True, to='quiz.QcmChoice'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='qcmsubmitone',
            name='id_selected',
            field=models.ForeignKey(null=True, to='quiz.QcmChoice'),
            preserve_default=True,
        ),
    ]
