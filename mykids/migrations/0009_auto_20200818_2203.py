# Generated by Django 2.2.5 on 2020-08-18 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mykids.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mykids', '0008_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(null=True, upload_to=mykids.models.generate_filename)),
                ('fav', models.BooleanField(default=False, verbose_name='Favoriet')),
                ('alltimefav', models.BooleanField(default=False, verbose_name='All time fav')),
                ('desc', models.CharField(blank=True, max_length=7000, null=True)),
                ('type', models.CharField(choices=[('Img', 'Image'), ('Vid', 'Video')], max_length=20, null=True)),
                ('order', models.IntegerField(blank=True, default=1, null=True)),
                ('dagboekpost', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mykids.DagboekPost')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
    ]
