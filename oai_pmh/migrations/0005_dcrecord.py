# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
        ('oai_pmh', '0004_resumptiontoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='DCRecord',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('header', models.OneToOneField(primary_key=True, serialize=False, to='oai_pmh.Header')),
                ('dc_title', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:title', blank=True)),
                ('dc_creator', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:creator', blank=True)),
                ('dc_subject', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:subject', blank=True)),
                ('dc_description', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:description', blank=True)),
                ('dc_publisher', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:publisher', blank=True)),
                ('dc_contributor', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:contributor', blank=True)),
                ('dc_date', models.DateTimeField(auto_now=True, verbose_name=' dc:date')),
                ('dc_type', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:type', blank=True)),
                ('dc_format', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:format', blank=True)),
                ('dc_identifier', oai_pmh.models.TextFieldSingleLine(verbose_name=' dc:identifier')),
                ('dc_source', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:source', blank=True)),
                ('dc_language', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:language', blank=True)),
                ('dc_relation', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:relation', blank=True)),
                ('dc_coverage', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:coverage', blank=True)),
                ('dc_rights', oai_pmh.models.TextFieldSingleLine(null=True, verbose_name=' dc:rights', blank=True)),
            ],
            options={
                'ordering': ('header',),
                'verbose_name': 'Dublin Core record',
            },
        ),
    ]
