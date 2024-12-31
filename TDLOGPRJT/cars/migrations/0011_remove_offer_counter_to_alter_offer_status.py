# Generated by Django 5.1.4 on 2024-12-16 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0010_alter_offer_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='counter_to',
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]