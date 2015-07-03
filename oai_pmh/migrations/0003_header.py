# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
        ('oai_pmh', '0002_set'),
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', oai_pmh.models.TextFieldSingleLine(unique=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('metadata_formats', models.ManyToManyField(related_name='identifiers', to='oai_pmh.MetadataFormat', blank=True)),
                ('sets', models.ManyToManyField(related_name='headers', to='oai_pmh.Set', blank=True)),
            ],
            options={
                'ordering': ('identifier',),
            },
        ),
    ]
