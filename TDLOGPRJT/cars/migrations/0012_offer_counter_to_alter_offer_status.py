# Generated by Django 5.1.4 on 2024-12-17 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0011_remove_offer_counter_to_alter_offer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='counter_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='counter_offers', to='cars.offer'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('countered', 'Countered'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]
