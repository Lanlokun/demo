# Generated by Django 3.2.17 on 2023-10-12 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corecode', '0009_auto_20231011_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='breakfast',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='lunch',
            field=models.BooleanField(default=False),
        ),
    ]
