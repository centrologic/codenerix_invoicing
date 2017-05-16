# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0017_haulier_name_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='salesalbaran',
            name='summary_delivery',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='Address delivery'),
        ),
        migrations.AddField(
            model_name='salesinvoice',
            name='summary_invoice',
            field=models.TextField(blank=True, max_length=256, null=True, verbose_name='Address invoice'),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='address_delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='order_sales_delivery', to='codenerix_invoicing.Address', verbose_name='Address delivery'),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='address_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='order_sales_invoice', to='codenerix_invoicing.Address', verbose_name='Address invoice'),
        ),
    ]
