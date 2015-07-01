# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0003_association'),
        ('app', '0002_associationhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.ManyToManyField(related_name='users', to='association.Language'),
        ),
    ]
