# Generated by Django 3.2.8 on 2021-10-17 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0016_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
