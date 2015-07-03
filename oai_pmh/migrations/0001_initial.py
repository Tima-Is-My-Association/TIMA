# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetadataFormat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prefix', oai_pmh.models.TextFieldSingleLine(unique=True)),
                ('schema', models.URLField(max_length=2048)),
                ('namespace', models.URLField(max_length=2048)),
            ],
            options={
                'ordering': ('prefix',),
            },
        ),
    ]
