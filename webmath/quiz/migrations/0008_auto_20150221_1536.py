# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_auto_20150221_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qcmsubmitmulti',
            old_name='id_qcm',
            new_name='id_question',
        ),
        migrations.RenameField(
            model_name='qcmsubmitone',
            old_name='id_qcm',
            new_name='id_question',
        ),
    ]
