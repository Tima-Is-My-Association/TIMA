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
            name='ResumptionToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expiration_date', models.DateTimeField()),
                ('complete_list_size', models.IntegerField(default=0)),
                ('cursor', models.IntegerField(default=0)),
                ('token', oai_pmh.models.TextFieldSingleLine(unique=True)),
            ],
            options={
                'ordering': ('expiration_date',),
            },
        ),
    ]
