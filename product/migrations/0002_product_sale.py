# Generated by Django 4.1.7 on 2023-03-31 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
