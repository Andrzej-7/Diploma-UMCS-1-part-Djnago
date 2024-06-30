# Generated by Django 5.0.1 on 2024-01-21 20:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0015_order_you_get'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='User',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='crypto_from',
            field=models.CharField(choices=[('ETH', 'eth'), ('XMR', 'xmr'), ('DAI', 'dai'), ('DASH', 'dash'), ('Dogecoin', 'dogecoin'), ('BTC', 'bitcoin')], max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='crypto_to',
            field=models.CharField(choices=[('ETH', 'eth'), ('XMR', 'xmr'), ('DAI', 'dai'), ('DASH', 'dash'), ('Dogecoin', 'dogecoin'), ('BTC', 'bitcoin')], max_length=255),
        ),
    ]
