# Generated by Django 4.1.7 on 2023-04-14 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_zipcode_alter_order_address_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='?', max_length=10),
        ),
    ]
