# Generated by Django 2.2.5 on 2020-07-14 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mykids', '0002_media_alltimefav'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='beschrijving',
            field=models.CharField(blank=True, max_length=7000, null=True),
        ),
    ]
