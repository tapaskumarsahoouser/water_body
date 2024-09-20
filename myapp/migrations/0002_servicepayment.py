# Generated by Django 5.1.1 on 2024-09-14 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, verbose_name='User Name')),
                ('service_name', models.CharField(max_length=50, null=True, verbose_name='Service Name')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Order Id')),
                ('token', models.CharField(blank=True, max_length=200, null=True, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pond_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.pond')),
            ],
        ),
    ]