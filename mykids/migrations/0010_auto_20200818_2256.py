# Generated by Django 2.2.5 on 2020-08-18 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mykids', '0009_auto_20200818_2203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='name',
            new_name='naam',
        ),
        migrations.AlterField(
            model_name='image',
            name='type',
            field=models.CharField(choices=[('Img', 'Image')], max_length=20, null=True),
        ),
    ]
