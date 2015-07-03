# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
        ('oai_pmh', '0002_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('spec', oai_pmh.models.TextFieldSingleLine(unique=True)),
                ('name', oai_pmh.models.TextFieldSingleLine()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
