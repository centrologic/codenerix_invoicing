# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-31 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0031_auto_20170831_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleslinealbaran',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
        migrations.AddField(
            model_name='saleslinebasket',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
        migrations.AddField(
            model_name='saleslineinvoice',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
        migrations.AddField(
            model_name='saleslineinvoicerectification',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
        migrations.AddField(
            model_name='saleslineorder',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
        migrations.AddField(
            model_name='saleslineticket',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
        migrations.AddField(
            model_name='saleslineticketrectification',
            name='removed',
            field=models.BooleanField(default=False, editable=False, verbose_name='Removed'),
        ),
    ]
