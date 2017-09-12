# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0015_sequence_sequencename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequence',
            name='sequenceName',
            field=models.CharField(max_length=100, verbose_name=b'Sequence name'),
        ),
    ]
