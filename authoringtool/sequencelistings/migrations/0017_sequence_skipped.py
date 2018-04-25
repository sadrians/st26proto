# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0016_auto_20170913_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='skipped',
            field=models.BooleanField(default=False, verbose_name=b'Skipped'),
            preserve_default=True,
        ),
    ]
