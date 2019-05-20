# Generated by Django 2.2.1 on 2019-05-16 00:16

import django.db.models.deletion
from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TogglUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='TogglClient',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TogglProject',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('is_billable', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ktools.TogglClient')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TogglEntry',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('uid', models.IntegerField()),
                ('start_ts', models.DateTimeField(blank=True, null=True)),
                ('end_ts', models.DateTimeField(blank=True, null=True)),
                ('duration_sec', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ktools.TogglProject')),
            ],
        ),
    ]
