# Generated by Django 4.1.11 on 2023-10-02 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0002_settlement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_payment',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='settlement',
            name='settled_amount',
            field=models.IntegerField(),
        ),
    ]
