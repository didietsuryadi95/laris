# Generated by Django 2.1.1 on 2018-11-11 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0020_voucher_min_odr_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucher',
            name='min_odr_weight',
        ),
    ]
