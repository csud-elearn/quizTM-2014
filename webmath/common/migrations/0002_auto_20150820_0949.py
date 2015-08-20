# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('avatar', models.ImageField(upload_to='avatars/', null=True, blank=True)),
                ('type', models.CharField(default='S', max_length=1, choices=[('S', 'Étudiant'), ('P', 'Professeur'), ('A', 'Administrateur')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to='common.Student', related_name='groups')),
                ('owner', models.ForeignKey(to='common.Teacher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='student',
            name='type',
            field=models.CharField(default='S', max_length=1, choices=[('S', 'Étudiant'), ('P', 'Professeur'), ('A', 'Administrateur')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='teacher',
            name='type',
            field=models.CharField(default='S', max_length=1, choices=[('S', 'Étudiant'), ('P', 'Professeur'), ('A', 'Administrateur')]),
            preserve_default=True,
        ),
    ]
