# Generated by Django 3.1.5 on 2021-02-22 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(null=True),
        ),
    ]