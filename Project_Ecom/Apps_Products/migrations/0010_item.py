# Generated by Django 3.2.8 on 2021-10-12 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0009_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.IntegerField(default=1)),
                ('option', models.BooleanField(default=True)),
            ],
        ),
    ]
