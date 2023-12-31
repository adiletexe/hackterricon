# Generated by Django 4.1.7 on 2023-06-25 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartxapp', '0006_alter_userprofile_doc_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='photo_reports')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='photoreport',
            field=models.ManyToManyField(blank=True, to='apartxapp.photo'),
        ),
    ]
