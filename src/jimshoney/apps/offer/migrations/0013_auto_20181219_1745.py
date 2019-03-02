# Generated by Django 2.1.1 on 2018-12-19 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0012_auto_20181214_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rangedestination',
            name='destination_type',
            field=models.CharField(blank=True, choices=[('', ''), ('all', 'All'), ('state', 'State'), ('district', 'District'), ('subdistrict', 'Subdistrict'), ('village', 'Village')], max_length=12),
        ),
    ]
