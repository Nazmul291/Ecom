# Generated by Django 3.2.8 on 2021-10-17 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0013_auto_20211016_1729'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='CartItem',
        ),
    ]
