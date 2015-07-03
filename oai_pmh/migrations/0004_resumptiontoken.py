# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
        ('oai_pmh', '0003_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumptionToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expiration_date', models.DateTimeField()),
                ('complete_list_size', models.IntegerField(default=0)),
                ('cursor', models.IntegerField(default=0)),
                ('token', oai_pmh.models.TextFieldSingleLine(unique=True)),
                ('from_timestamp', models.DateTimeField(blank=True, null=True)),
                ('until_timestamp', models.DateTimeField(blank=True, null=True)),
                ('metadata_prefix', models.ForeignKey(null=True, to='oai_pmh.MetadataFormat', blank=True)),
                ('set_spec', models.ForeignKey(null=True, to='oai_pmh.Set', blank=True)),
            ],
            options={
                'ordering': ('expiration_date',),
            },
        ),
    ]
