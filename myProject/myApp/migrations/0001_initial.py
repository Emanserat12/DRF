# Generated by Django 5.0.7 on 2024-07-25 04:57

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('inStock', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('category', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('orderedAt', models.BigIntegerField()),
                ('noOfItems', models.IntegerField()),
                ('totalBill', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.products')),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
