# Generated by Django 5.0 on 2023-12-29 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_cartorder_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
