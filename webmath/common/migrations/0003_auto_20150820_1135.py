# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150820_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to='common.Student', related_name='classes')),
                ('owner', models.ForeignKey(to='common.Teacher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='classes',
            name='members',
        ),
        migrations.RemoveField(
            model_name='classes',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Classes',
        ),
    ]
