# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-04 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0037_reasonmodification_reasonmodificationlinealbaran_reasonmodificationlinebasket_reasonmodificationline'),
    ]

    operations = [
        migrations.AddField(
            model_name='reasonmodificationlinealbaran',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonmodificationlinebasket',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonmodificationlineinvoice',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonmodificationlineinvoicerectification',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonmodificationlineorder',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonmodificationlineticket',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reasonmodificationlineticketrectification',
            name='quantity',
            field=models.FloatField(default=0, verbose_name='Quantity'),
            preserve_default=False,
        ),
    ]