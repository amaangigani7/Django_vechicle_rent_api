# Generated by Django 4.1.3 on 2022-11-08 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_customer_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="number_plate",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
