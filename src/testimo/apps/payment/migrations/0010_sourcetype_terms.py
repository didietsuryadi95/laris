# Generated by Django 2.0 on 2019-03-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20190222_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcetype',
            name='terms',
            field=models.TextField(blank=True, null=True, verbose_name='Terms & Conditions'),
        ),
    ]
