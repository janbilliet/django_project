# Generated by Django 3.0.6 on 2021-09-12 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mykids', '0015_auto_20210430_2323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dagboekpost',
            old_name='beschrijving',
            new_name='beschrijving_lotte',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='gewicht',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='lengte',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='nachtflesjes',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='sprong',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='uurvanOpstaan',
        ),
        migrations.RemoveField(
            model_name='dagboekpost',
            name='uurvanSlapen',
        ),
        migrations.AddField(
            model_name='dagboekpost',
            name='beschrijving_merlijn',
            field=models.CharField(blank=True, max_length=7000, null=True),
        ),
    ]
