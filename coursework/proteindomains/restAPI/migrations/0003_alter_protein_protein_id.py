# Generated by Django 3.2.4 on 2021-06-28 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0002_alter_protein_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protein',
            name='protein_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
