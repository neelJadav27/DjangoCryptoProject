# Generated by Django 4.0.3 on 2022-04-01 02:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0007_remove_wallet_cumulativeamount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='paymentDate',
            field=models.DateField(default=datetime.datetime(2022, 3, 31, 22, 18, 49, 705042)),
        ),
    ]
