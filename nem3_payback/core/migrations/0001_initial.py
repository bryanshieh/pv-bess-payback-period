# Generated by Django 5.1.4 on 2024-12-13 19:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('start_interval', models.DateTimeField(auto_now_add=True)),
                ('end_interval', models.DateTimeField(auto_now_add=True)),
                ('reading_kwh', models.DecimalField(decimal_places=4, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='RateSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('rate_code', models.CharField(max_length=10)),
                ('rate_dollars_kwh', models.DecimalField(decimal_places=4, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nem_version', models.CharField(max_length=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rate_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254)),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SystemConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_capacity_kwh', models.DecimalField(decimal_places=3, max_digits=6)),
                ('solar_panel_capacity_kw', models.DecimalField(decimal_places=3, max_digits=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userupload')),
            ],
        ),
    ]
