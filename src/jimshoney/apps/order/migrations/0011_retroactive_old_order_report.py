from __future__ import unicode_literals

from django.db import migrations
from apps.order.processing import EventHandler
from oscar.core.loading import get_model

Order = get_model('order', 'Order')


def retroactive_old_order_status(apps, schema_editor):
    handler = EventHandler()
    approved_order = Order.objects.exclude(status__in=['Placed', 'Canceled'])
    for o in approved_order:
        try:
            handler.create_order_report(o)
        except:
            print('failed')


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_orderreport_date_placed'),
    ]

    operations = [
        migrations.RunPython(retroactive_old_order_status),
    ]
