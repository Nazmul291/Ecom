# Generated by Django 3.2.8 on 2021-10-13 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0011_item_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='user',
            field=models.IntegerField(default=1),
        ),
    ]
