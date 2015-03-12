# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedQuiz',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Qcm',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('points', models.FloatField(default=1)),
                ('number', models.IntegerField()),
                ('multi_answers', models.BooleanField()),
                ('show_list', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QcmChoice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('valid', models.BooleanField()),
                ('id_question', models.ForeignKey(to='quiz.Qcm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QcmSubmitMulti',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('result', models.FloatField(default=0)),
                ('id_question', models.ForeignKey(to='quiz.Qcm')),
                ('id_selected', models.ManyToManyField(null=True, to='quiz.QcmChoice')),
                ('id_submitted_quiz', models.ForeignKey(to='quiz.CompletedQuiz')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QcmSubmitOne',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('result', models.FloatField(default=0)),
                ('id_question', models.ForeignKey(to='quiz.Qcm')),
                ('id_selected', models.ForeignKey(null=True, to='quiz.QcmChoice')),
                ('id_submitted_quiz', models.ForeignKey(to='quiz.CompletedQuiz')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=1000)),
                ('id_teacher', models.ForeignKey(to='common.Teacher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizDraft',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimpleQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('points', models.FloatField(default=1)),
                ('number', models.IntegerField()),
                ('id_quiz', models.ForeignKey(to='quiz.Quiz')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SqAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('id_question', models.ForeignKey(to='quiz.SimpleQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SqSubmit',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('result', models.FloatField(default=0)),
                ('id_question', models.ForeignKey(to='quiz.SimpleQuestion')),
                ('id_submitted_quiz', models.ForeignKey(to='quiz.CompletedQuiz')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='qcm',
            name='id_quiz',
            field=models.ForeignKey(to='quiz.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='id_quiz',
            field=models.ForeignKey(to='quiz.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='id_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
