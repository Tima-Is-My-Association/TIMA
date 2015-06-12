# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import association.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', association.models.TextFieldSingleLine(unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('code', association.models.TextFieldSingleLine(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
