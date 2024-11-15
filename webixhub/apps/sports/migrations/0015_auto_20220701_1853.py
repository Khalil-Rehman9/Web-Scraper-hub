# Generated by Django 3.2.11 on 2022-07-01 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0014_alter_footballmatch_league_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='footballmatch',
            name='match_details',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='match_league_id',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='prev_match',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='team_1_id',
        ),
        migrations.RemoveField(
            model_name='footballmatch',
            name='team_2_id',
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_form',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_info',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_logo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_url',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_form',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_info',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_logo',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_url',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='kampinfo',
            field=models.TextField(null=True),
        ),
    ]
