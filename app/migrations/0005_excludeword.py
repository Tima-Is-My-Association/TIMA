# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0003_association'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_newsletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcludeWord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='association.Word')),
            ],
            options={
                'ordering': ('user', 'updated_at'),
            },
        ),
    ]
