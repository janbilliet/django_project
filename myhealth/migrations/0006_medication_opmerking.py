# Generated by Django 2.2.5 on 2020-10-01 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myhealth', '0005_medication_medicatie'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='opmerking',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
