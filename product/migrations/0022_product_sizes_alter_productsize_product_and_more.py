# Generated by Django 4.1.7 on 2023-04-23 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_productsize_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, through='product.ProductSize', to='product.size'),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_quantities', to='product.product'),
        ),
        migrations.AlterField(
            model_name='productsize',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.size'),
        ),
    ]