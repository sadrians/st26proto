# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0014_auto_20161217_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='sequence',
            name='sequenceName',
            field=models.CharField(default=b'seq_', max_length=100, verbose_name=b'Sequence name'),
            preserve_default=True,
        ),
    ]
