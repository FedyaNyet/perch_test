# Generated by Django 3.1 on 2021-10-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20211002_0455'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='fbatransaction',
            index=models.Index(fields=['total'], name='fba_transac_total_9cffa6_idx'),
        ),
    ]
