# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oai_pmh', '0003_metadataformat'),
    ]

    operations = [
        migrations.AddField(
            model_name='header',
            name='metadata_formats',
            field=models.ManyToManyField(related_name='identifiers', to='oai_pmh.MetadataFormat'),
        ),
    ]
