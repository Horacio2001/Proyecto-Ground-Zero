# Generated by Django 5.0.6 on 2024-06-27 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_voucher_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
