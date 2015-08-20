# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('avatar', models.ImageField(null=True, blank=True, upload_to='avatars/')),
                ('type', models.CharField(max_length=1, choices=[('S', 'Étudiant'), ('P', 'Professeur'), ('A', 'Administrateur')], default='S')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('baseprofile_ptr', models.OneToOneField(primary_key=True, to='common.BaseProfile', parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=('common.baseprofile',),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('baseprofile_ptr', models.OneToOneField(primary_key=True, to='common.BaseProfile', parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=('common.baseprofile',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('baseprofile_ptr', models.OneToOneField(primary_key=True, to='common.BaseProfile', parent_link=True, auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=('common.baseprofile',),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', to='common.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(to='common.Teacher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile'),
            preserve_default=True,
        ),
    ]
