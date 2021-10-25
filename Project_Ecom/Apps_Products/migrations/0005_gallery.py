# Generated by Django 3.2.8 on 2021-10-10 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Apps_Products', '0004_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(blank=True, null=True, upload_to='gallery')),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Apps_Products.product')),
            ],
        ),
    ]