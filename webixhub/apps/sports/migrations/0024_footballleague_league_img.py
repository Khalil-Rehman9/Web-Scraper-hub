# Generated by Django 3.2.11 on 2022-08-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0023_auto_20220812_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballleague',
            name='league_img',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
