# Generated by Django 3.2.4 on 2021-06-29 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restAPI', '0007_auto_20210629_0857'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='proteindomain',
            name='unique_domain_within_protein',
        ),
        migrations.RenameField(
            model_name='proteindomain',
            old_name='domain_id',
            new_name='pfam_id',
        ),
        migrations.AddConstraint(
            model_name='proteindomain',
            constraint=models.UniqueConstraint(fields=('protein_id', 'pfam_id', 'start', 'stop'), name='unique_domain_within_protein'),
        ),
    ]