# Generated by Django 4.1.7 on 2023-05-10 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='index',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=30),
        ),
    ]