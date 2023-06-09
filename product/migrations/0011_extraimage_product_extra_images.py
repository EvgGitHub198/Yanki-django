# Generated by Django 4.1.7 on 2023-04-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/extra_images')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='extra_images',
            field=models.ManyToManyField(blank=True, related_name='products', to='product.extraimage'),
        ),
    ]
