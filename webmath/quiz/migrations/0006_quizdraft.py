# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20150102_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizDraft',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
