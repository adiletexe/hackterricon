# Generated by Django 4.1.7 on 2023-06-25 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartxapp', '0007_photo_order_photoreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
