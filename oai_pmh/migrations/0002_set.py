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
            name='Set',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('spec', oai_pmh.models.TextFieldSingleLine(unique=True)),
                ('name', oai_pmh.models.TextFieldSingleLine()),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
