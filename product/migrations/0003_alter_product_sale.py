# Generated by Django 4.1.7 on 2023-03-31 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
