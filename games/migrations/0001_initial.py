# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import games.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('association', '0003_association'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationChain',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chain_id', models.PositiveIntegerField(default=games.models.default_chain_id)),
                ('previous', models.ForeignKey(null=True, to='games.AssociationChain', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='association.Word')),
            ],
            options={
                'ordering': ('chain_id', 'id'),
            },
        ),
    ]
