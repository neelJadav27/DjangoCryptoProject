# Generated by Django 4.0.3 on 2022-04-04 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0016_alter_wallet_paymentdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='walletBalance',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=100),
        ),
    ]
