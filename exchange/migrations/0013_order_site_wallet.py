# Generated by Django 4.2.7 on 2023-11-08 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0012_alter_order_crypto_from_alter_order_crypto_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='site_wallet',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
