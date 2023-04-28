# Generated by Django 4.1.7 on 2023-04-26 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_product_sizes_alter_productsize_product_and_more'),
        ('order', '0009_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='product.product'),
        ),
    ]