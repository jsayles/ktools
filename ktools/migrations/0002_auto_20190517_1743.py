# Generated by Django 2.2.1 on 2019-05-17 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ktools', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='togglentry',
            name='duration_sec',
            field=models.IntegerField(default=0),
        ),
    ]
