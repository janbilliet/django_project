# Generated by Django 3.0.6 on 2021-09-18 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mykids', '0018_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='alltimefav',
        ),
        migrations.RemoveField(
            model_name='image',
            name='fav',
        ),
        migrations.RemoveField(
            model_name='video',
            name='alltimefav',
        ),
        migrations.RemoveField(
            model_name='video',
            name='fav',
        ),
        migrations.AddField(
            model_name='image',
            name='rating',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mykids.Rating'),
        ),
        migrations.AddField(
            model_name='video',
            name='rating',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mykids.Rating'),
        ),
    ]
