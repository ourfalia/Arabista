# Generated by Django 3.2.19 on 2023-06-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meals',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
