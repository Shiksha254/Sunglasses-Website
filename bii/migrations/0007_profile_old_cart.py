# Generated by Django 5.0.1 on 2024-04-11 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bii', '0006_rename_customer_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
