# Generated by Django 5.0.2 on 2024-02-24 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_data_creation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='return',
            name='access_of_return',
        ),
        migrations.AlterField(
            model_name='return',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='returns', to='shop.order'),
        ),
    ]
