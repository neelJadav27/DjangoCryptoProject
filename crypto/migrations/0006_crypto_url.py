# Generated by Django 4.0.3 on 2022-03-25 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0005_alter_crypto_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='url',
            field=models.TextField(default='https://raw.githubusercontent.com/neelJadav27/DjangoCryptoProject/main/NoImage.png'),
        ),
    ]
