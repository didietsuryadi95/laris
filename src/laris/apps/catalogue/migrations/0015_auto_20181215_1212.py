# Generated by Django 2.0 on 2018-12-15 05:12

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_product_highlight'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('all', django.db.models.manager.Manager()),
            ],
        ),
    ]
