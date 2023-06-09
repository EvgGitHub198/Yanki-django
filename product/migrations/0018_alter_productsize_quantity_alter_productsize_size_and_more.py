# Generated by Django 4.1.7 on 2023-04-21 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_remove_size_quantity_productsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsize',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_sizes', to='product.size'),
        ),
        migrations.AlterUniqueTogether(
            name='productsize',
            unique_together={('product', 'size')},
        ),
    ]
