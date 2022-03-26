# Generated by Django 4.0.3 on 2022-03-23 23:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_user_dob_alter_user_phoneno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phoneNo',
            field=models.PositiveIntegerField(default=1111111111, validators=[django.core.validators.RegexValidator(message='THIS WILL ONLY ALLOW TEN DIGIT NUMBERS', regex='^[0-9]{10}$')]),
            preserve_default=False,
        ),
    ]