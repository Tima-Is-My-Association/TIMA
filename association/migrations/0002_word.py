# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import association.models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', association.models.TextFieldSingleLine()),
                ('count', models.BigIntegerField(default=0)),
                ('language', models.ForeignKey(related_name='words', to='association.Language')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='word',
            unique_together=set([('name', 'language')]),
        ),
    ]
