# Generated by Django 5.1.4 on 2024-12-17 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0013_remove_offer_counter_to_offer_counter_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='counter_amount',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='counter_message',
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]