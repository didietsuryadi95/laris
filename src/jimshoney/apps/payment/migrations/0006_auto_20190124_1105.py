# Generated by Django 2.0 on 2019-01-24 04:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20190117_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='source',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Created'),
        ),
        migrations.AddField(
            model_name='source',
            name='payment_status',
            field=models.CharField(choices=[('1', 'Payment Success'), ('0', 'Payment Failed'), ('6', 'Payment Pending'), ('99', 'Payment Initiated')], default='99', max_length=2, verbose_name='Payment Status'),
        ),
        migrations.AddField(
            model_name='source',
            name='va_expired',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Virtual Account Expired Date'),
        ),
        migrations.AddField(
            model_name='source',
            name='va_number',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Virtual Account Number'),
        ),
        migrations.AlterField(
            model_name='sourcetype',
            name='code',
            field=models.CharField(max_length=32, verbose_name='Bank Code'),
        ),
        migrations.AlterField(
            model_name='sourcetype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Bank Image'),
        ),
        migrations.AlterField(
            model_name='sourcetype',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Payment Available?'),
        ),
        migrations.AlterField(
            model_name='sourcetype',
            name='source_type',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Payment Method'),
        ),
    ]
