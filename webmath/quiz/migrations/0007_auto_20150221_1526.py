# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_quizdraft'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qcmchoice',
            old_name='id_qcm',
            new_name='id_question',
        ),
    ]
