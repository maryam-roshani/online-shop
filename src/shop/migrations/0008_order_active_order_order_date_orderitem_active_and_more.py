# Generated by Django 4.0 on 2022-12-24 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_item_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='costumer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.user'),
        ),
        migrations.AlterField(
            model_name='order',
            name='costumer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.user'),
        ),
    ]
