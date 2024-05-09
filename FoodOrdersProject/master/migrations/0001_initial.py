# Generated by Django 5.0.4 on 2024-05-09 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': '"food_orders"."categories"',
            },
        ),
        migrations.CreateModel(
            name='Medias',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('type', models.CharField(max_length=100)),
                ('size', models.IntegerField()),
            ],
            options={
                'db_table': '"food_orders"."medias"',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('prefix_code', models.CharField(choices=[('BNK', 'Bank'), ('GJK', 'Gojek'), ('DNA', 'Dana'), ('OVO', 'Ovo'), ('SHP', 'Shopee')], default='', max_length=3)),
            ],
            options={
                'db_table': '"food_orders"."payment_methods"',
            },
        ),
        migrations.CreateModel(
            name='Promos',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': '"food_orders"."promos"',
            },
        ),
        migrations.CreateModel(
            name='HomeBanners',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('media_id', models.OneToOneField(db_column='media_id', on_delete=django.db.models.deletion.RESTRICT, to='master.medias')),
            ],
            options={
                'db_table': '"food_orders"."home_banners"',
            },
        ),
    ]
