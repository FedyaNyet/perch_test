# Generated by Django 3.1 on 2021-10-03 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20211003_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbatransaction',
            name='kind',
            field=models.CharField(blank=True, choices=[('Order', 'Order'), ('FBA Inventory Fee', 'FBA Inventory Fee'), ('Adjustment', 'Adjustment')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='tid',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
