# Generated by Django 3.2.8 on 2021-10-13 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0010_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ImageField(default=1, upload_to=''),
        ),
    ]
