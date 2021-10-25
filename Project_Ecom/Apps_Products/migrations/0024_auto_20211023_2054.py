# Generated by Django 3.2.8 on 2021-10-23 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Apps_Products', '0023_remove_price_sub_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eligible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used', models.BooleanField(default=False)),
                ('cupon_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Apps_Products.cupon')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='discount',
            name='cupon_code',
        ),
        migrations.RemoveField(
            model_name='discount',
            name='used',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='discount',
            name='discount',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='Price',
        ),
    ]
