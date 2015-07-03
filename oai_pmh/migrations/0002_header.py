# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
        ('oai_pmh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', oai_pmh.models.TextFieldSingleLine(unique=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('metadata_formats', models.ManyToManyField(to='oai_pmh.MetadataFormat', related_name='identifiers')),
            ],
            options={
                'ordering': ('identifier',),
            },
        ),
    ]
