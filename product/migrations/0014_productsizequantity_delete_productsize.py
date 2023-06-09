# Generated by Django 4.1.7 on 2023-04-21 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_productsize'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSizeQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_quantities', to='product.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.size')),
            ],
        ),
        migrations.DeleteModel(
            name='ProductSize',
        ),
    ]
