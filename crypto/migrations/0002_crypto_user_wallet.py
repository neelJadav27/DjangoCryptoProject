# Generated by Django 4.0.3 on 2022-03-15 04:04

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crypto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alias', models.CharField(max_length=30)),
                ('available', models.PositiveIntegerField(default=1000)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phoneNo', models.PositiveIntegerField(validators=[django.core.validators.RegexValidator(message='THIS WILL ONLY ALLOW TEN DIGIT NUMBERS', regex='^[0-9]{10}$')])),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default='F', max_length=1)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currRate', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('cumulativeAmount', models.PositiveIntegerField()),
                ('sold', models.PositiveIntegerField()),
                ('crypto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto.crypto')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto.user')),
            ],
        ),
    ]