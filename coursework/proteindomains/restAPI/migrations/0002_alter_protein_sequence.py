# Generated by Django 3.2.4 on 2021-06-27 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protein',
            name='sequence',
            field=models.CharField(max_length=35991, null=True),
        ),
    ]
