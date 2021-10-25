# Generated by Django 3.2.8 on 2021-10-24 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0025_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='cupon_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Apps_Products.cupon'),
        ),
        migrations.AddField(
            model_name='discount',
            name='used',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Eligible',
        ),
    ]
