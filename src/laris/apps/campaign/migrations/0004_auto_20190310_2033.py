# Generated by Django 2.0 on 2019-03-10 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0003_auto_20190211_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='oss_image_desktop',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='oss_image_mobile',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='bannermini',
            name='oss_image',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='endorsement',
            name='oss_image',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
