# Generated by Django 3.1 on 2021-10-02 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbatransaction',
            name='tid',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
