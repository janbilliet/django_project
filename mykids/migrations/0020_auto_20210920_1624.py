# Generated by Django 3.0.6 on 2021-09-20 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mykids', '0019_auto_20210918_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='rating',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mykids.Rating'),
        ),
        migrations.AlterField(
            model_name='video',
            name='rating',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mykids.Rating'),
        ),
    ]
