# Generated by Django 3.2.8 on 2021-10-17 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0015_alter_cartitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.ImageField(default=1, upload_to=''),
        ),
    ]
