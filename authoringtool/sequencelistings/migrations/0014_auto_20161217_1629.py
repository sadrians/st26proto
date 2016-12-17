# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequencelistings', '0013_auto_20160802_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencelisting',
            name='applicantNameLatin',
            field=models.CharField(max_length=200, verbose_name=b'Applicant name Latin', blank=True),
        ),
    ]
