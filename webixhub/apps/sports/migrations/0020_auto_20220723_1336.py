# Generated by Django 3.2.11 on 2022-07-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0019_auto_20220702_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='footballteam',
            old_name='team_unique_id',
            new_name='bold_team_id',
        ),
        migrations.RenameField(
            model_name='footballteam',
            old_name='tournament_history',
            new_name='fixtures',
        ),
        migrations.AddField(
            model_name='footballteam',
            name='results',
            field=models.JSONField(null=True),
        ),
    ]
