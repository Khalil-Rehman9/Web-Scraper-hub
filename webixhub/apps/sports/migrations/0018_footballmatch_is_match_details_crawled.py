# Generated by Django 3.2.11 on 2022-07-02 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0017_auto_20220702_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballmatch',
            name='is_match_details_crawled',
            field=models.IntegerField(default=0, max_length=4, null=True),
        ),
    ]
