# Generated by Django 4.0.3 on 2022-03-25 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0004_alter_user_phoneno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
