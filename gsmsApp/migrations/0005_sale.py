# Generated by Django 4.0.3 on 2022-04-16 05:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gsmsApp', '0004_stock_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('customer_name', models.CharField(max_length=250)),
                ('volume', models.FloatField(default=0, max_length=(15, 2))),
                ('amount', models.FloatField(default=0, max_length=(15, 2))),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('petrol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gsmsApp.petrol')),
            ],
            options={
                'verbose_name_plural': 'List of Sales',
            },
        ),
    ]