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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', association.models.TextFieldSingleLine(unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('count', models.BigIntegerField(default=0)),
                ('languages', models.ManyToManyField(to='association.Language', related_name='words')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
