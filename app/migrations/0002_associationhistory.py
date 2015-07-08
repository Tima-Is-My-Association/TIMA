# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0003_association'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('points', models.FloatField(default=0)),
                ('association', models.ForeignKey(to='association.Association')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
                'ordering': ('user',),
            },
        ),
    ]
