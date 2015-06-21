# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def default_pages(apps, schema_editor):
    Page = apps.get_model('pages', 'Page')
    Page.objects.create(slug='imprint', title='Imprint', text='<p>Edit content.</p>')


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_pages),
    ]
