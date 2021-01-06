# Generated by Django 2.2.5 on 2020-07-31 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myfinances', '0002_auto_20200718_1204'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='name',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
