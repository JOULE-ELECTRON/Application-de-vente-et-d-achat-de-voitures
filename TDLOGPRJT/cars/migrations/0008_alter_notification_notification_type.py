# Generated by Django 5.1.4 on 2024-12-16 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_notification_offer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('trade_offer', 'Trade Offer'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('offer_rejected', 'Offer Rejected')], max_length=20),
        ),
    ]
