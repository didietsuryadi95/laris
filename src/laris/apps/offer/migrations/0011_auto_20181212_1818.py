# Generated by Django 2.1.1 on 2018-12-12 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0010_condition_range_destination'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='range_destination',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='offer.RangeDestination'),
        ),
    ]
