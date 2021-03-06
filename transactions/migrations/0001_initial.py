# Generated by Django 3.1 on 2021-10-02 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FBATransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('kind', models.CharField(blank=True, max_length=32, null=True)),
                ('sku', models.CharField(blank=True, max_length=32, null=True)),
                ('description', models.CharField(blank=True, max_length=32, null=True)),
                ('quantity', models.IntegerField(null=True)),
                ('city', models.CharField(blank=True, max_length=32, null=True)),
                ('state', models.CharField(blank=True, max_length=32, null=True)),
                ('postal', models.CharField(blank=True, max_length=32, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=13, null=True)),
            ],
            options={
                'db_table': 'fba_transactions',
            },
        ),
    ]
