# Generated by Django 3.2.11 on 2022-06-22 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0013_rename_match_league_id_footballleague_league_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballmatch',
            name='league_id',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
