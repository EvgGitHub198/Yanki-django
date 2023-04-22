# Generated by Django 4.1.7 on 2023-04-21 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_orderitem_selected_size_orderitem_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped')], default='processing', max_length=20),
        ),
    ]