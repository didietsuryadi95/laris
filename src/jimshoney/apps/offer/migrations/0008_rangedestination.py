# Generated by Django 2.1.1 on 2018-12-11 10:42

from django.db import migrations, models
import oscar.models.fields.autoslugfield


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0007_conditionaloffer_exclusive'),
    ]

    operations = [
        migrations.CreateModel(
            name='RangeDestination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('slug', oscar.models.fields.autoslugfield.AutoSlugField(blank=True, editable=False, max_length=128, populate_from='name', unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True)),
                ('destination_type', models.CharField(blank=True, choices=[('', '---------'), ('state', 'State'), ('district', 'District'), ('subdistrict', 'Subdistrict'), ('village', 'Village')], max_length=12)),
                ('destination_id', models.IntegerField(blank=True, default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
            ],
            options={
                'verbose_name': 'Destination Range',
                'verbose_name_plural': 'Destination Ranges',
                'db_table': 'offer_range_destination',
            },
        ),
    ]
