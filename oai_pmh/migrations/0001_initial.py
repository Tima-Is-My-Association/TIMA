# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oai_pmh.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('identifier', oai_pmh.models.TextFieldSingleLine()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('identifier',),
            },
        ),
    ]
