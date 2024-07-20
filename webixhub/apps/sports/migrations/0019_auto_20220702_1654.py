# Generated by Django 3.2.11 on 2022-07-02 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0018_footballmatch_is_match_details_crawled'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballmatch',
            name='away_team',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='away_team_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='home_team_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footballmatch',
            name='match_details_json',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='footballmatch',
            name='is_match_details_crawled',
            field=models.IntegerField(max_length=4, null=True),
        ),
    ]
