# Generated by Django 4.0.3 on 2022-04-04 04:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0014_alter_wallet_paymentdate_alter_wallet2_paymentdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='paymentDate',
            field=models.DateField(default=datetime.datetime(2022, 4, 4, 4, 52, 42, 866046, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='Wallet2',
        ),
    ]
