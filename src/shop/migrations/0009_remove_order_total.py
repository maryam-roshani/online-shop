# Generated by Django 4.0 on 2022-12-24 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_order_active_order_order_date_orderitem_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
    ]
