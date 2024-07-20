# Generated by Django 3.2.11 on 2022-07-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0016_auto_20220701_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballmatch',
            name='away_team_form',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='away_team_info',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='away_team_logo',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='away_team_name',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='away_team_url',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='home_team_form',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='home_team_info',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='home_team_logo',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='home_team_name',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='home_team_url',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='league_url',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='match_kampinfo',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='match_odds',
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='bolddk_match_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
