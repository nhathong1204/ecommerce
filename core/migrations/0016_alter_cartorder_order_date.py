# Generated by Django 5.0 on 2023-12-29 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_wishlist_rating_remove_wishlist_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(),
        ),
    ]