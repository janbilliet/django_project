# Generated by Django 2.2.5 on 2020-08-07 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mykids', '0005_auto_20200807_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='name',
            new_name='naam',
        ),
    ]
