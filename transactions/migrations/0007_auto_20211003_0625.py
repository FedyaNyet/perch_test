# Generated by Django 3.1.2 on 2021-10-03 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20211003_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fbatransaction',
            name='city',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='description',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='kind',
            field=models.CharField(choices=[('Order', 'Order'), ('FBA Inventory Fee', 'FBA Inventory Fee'), ('Adjustment', 'Adjustment'), ('FBA Customer Return Fee', 'FBA Customer Return Fee'), ('Transfer', 'Transfer'), ('Refund', 'Refund'), ('Order_Retrocharge', 'Order_Retrocharge')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='postal',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='sku',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='state',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='tid',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='fbatransaction',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
