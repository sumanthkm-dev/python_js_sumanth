# Generated by Django 5.1.2 on 2024-10-14 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_number', models.IntegerField(unique=True)),
                ('item_desc', models.TextField()),
                ('category', models.IntegerField()),
                ('category_name', models.CharField(max_length=200)),
                ('vendor_number', models.IntegerField()),
                ('vendor_name', models.CharField(max_length=200)),
                ('pack', models.IntegerField()),
                ('bottle_volume_ml', models.IntegerField()),
                ('state_bottle_cost', models.FloatField()),
                ('state_bottle_retail', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_number', models.IntegerField(unique=True)),
                ('store_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.IntegerField()),
                ('store_location', models.CharField(max_length=200)),
                ('county_number', models.IntegerField()),
                ('county', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=200, unique=True)),
                ('date', models.DateField()),
                ('bottles_sold', models.IntegerField()),
                ('sale_dollars', models.FloatField()),
                ('volume_sold_liters', models.FloatField()),
                ('volume_sold_gallons', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesapp.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salesapp.store')),
            ],
        ),
    ]