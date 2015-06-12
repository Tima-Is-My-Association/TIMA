# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0002_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('count', models.BigIntegerField(default=0)),
                ('association', models.ForeignKey(related_name='association', to='association.Word')),
                ('word', models.ForeignKey(related_name='word', to='association.Word')),
            ],
            options={
                'ordering': ('word', 'association'),
            },
        ),
    ]
