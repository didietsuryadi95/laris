# Generated by Django 2.1.1 on 2018-12-20 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0018_auto_20181220_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rangedestination',
            name='destination_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
