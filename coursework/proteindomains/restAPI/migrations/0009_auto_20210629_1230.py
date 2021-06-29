# Generated by Django 3.2.4 on 2021-06-29 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0008_auto_20210629_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protein',
            name='length',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='protein',
            name='taxonomy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='organisms', to='restAPI.organism'),
        ),
    ]