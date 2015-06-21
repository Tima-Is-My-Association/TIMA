# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pages.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True, max_length=2048)),
                ('title', pages.models.TextFieldSingleLine()),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
