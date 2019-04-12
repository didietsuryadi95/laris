# Generated by Django 2.0 on 2019-04-11 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0005_auto_20190320_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoFooter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Seo Footer',
                'verbose_name_plural': 'Seo Footers',
                'ordering': ['-date_created'],
            },
        ),
    ]
