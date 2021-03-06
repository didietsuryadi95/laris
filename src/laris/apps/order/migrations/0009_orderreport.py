# Generated by Django 2.0 on 2019-02-22 07:00

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_auto_20190222_1400'),
        ('order', '0008_auto_20190128_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('number', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Order number')),
                ('order_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Order Amount')),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Shipping_cost')),
                ('product_promo', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Product Promo')),
                ('shipping_promo', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Shipping Promo')),
                ('total_order', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Total Order')),
                ('payment_method', models.CharField(max_length=128, verbose_name='Payment Method')),
                ('percent_fee', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Percent Fee')),
                ('gdn_percent_fee', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='GDN Percent Fee')),
                ('bank_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Bank Fee')),
                ('gdn_bank_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='GDN Bank Fee')),
                ('amount_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Amount Fee')),
                ('gdn_amount_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='GDN Amount Fee')),
                ('ipay_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Ipay Cost')),
                ('tax_vat', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Tax VAT')),
                ('tax_pph23', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Tax PPH23')),
                ('total_ipay_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Total IPAY Cost')),
                ('gdn_fee_percent', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='GDN Fee Percent')),
                ('total_gdn_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Total GDN Fee')),
                ('income_ipay', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Income IPay')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('source_type', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='payment.SourceType')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
