# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-23 08:36
from __future__ import unicode_literals
from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0020_auto_20180515_1333'),
    ]

    def run_migrate(apps, schema_editor):
        model = apps.get_model('codenerix_invoicing', 'SalesLines')
        for line in model.objects.all():
            line.price_unit_basket = line.total_basket / Decimal(line.quantity)
            line.price_unit_order = line.total_order / Decimal(line.quantity)
            line.price_unit_ticket = line.total_ticket / Decimal(line.quantity)
            line.price_unit_invoice = line.total_invoice / Decimal(line.quantity)
            line.save()

    operations = [
        migrations.AddField(
            model_name='saleslines',
            name='price_unit_basket',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='unit_price'),
        ),
        migrations.AddField(
            model_name='saleslines',
            name='price_unit_invoice',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='unit_price'),
        ),
        migrations.AddField(
            model_name='saleslines',
            name='price_unit_order',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='unit_price'),
        ),
        migrations.AddField(
            model_name='saleslines',
            name='price_unit_ticket',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='unit_price'),
        ),
        migrations.RunPython(run_migrate),
    ]
