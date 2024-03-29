# Generated by Django 2.0 on 2019-03-20 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_auto_20190310_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image_desktop',
            field=models.ImageField(blank=True, null=True, upload_to='campaign/banner/', verbose_name='Image Desktop'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='image_mobile',
            field=models.ImageField(blank=True, null=True, upload_to='campaign/banner/', verbose_name='Image Mobile'),
        ),
        migrations.AlterField(
            model_name='bannermini',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='campaign/banner_mini/', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='endorsement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='campaign/endorsement/', verbose_name='Image'),
        ),
    ]
