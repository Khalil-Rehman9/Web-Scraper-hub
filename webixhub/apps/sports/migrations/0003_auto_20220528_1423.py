# Generated by Django 3.2.11 on 2022-05-28 14:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0002_footballmatch_parsed_match_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballbookmaker',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='footballmatch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
