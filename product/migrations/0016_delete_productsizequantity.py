# Generated by Django 4.1.7 on 2023-04-21 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_size_quantity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductSizeQuantity',
        ),
    ]