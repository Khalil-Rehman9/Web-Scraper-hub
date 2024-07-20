from django.db import models

# Create your models here.
class Source(models.Model):
    source_name = models.CharField(max_length=100)
    source_url = models.CharField(max_length=255)
    status = models.SmallIntegerField(max_length=2, default=1)

class FootballMatch(models.Model):
    source_id = models.IntegerField(max_length=11)
    match_unique_id = models.CharField(max_length=100,null=True)
    bolddk_match_id = models.CharField(max_length=100,null=True)
    match_date = models.CharField(max_length=250, null=True)
    match_time = models.CharField(max_length=250, null=True)
    parsed_match_date_time = models.DateTimeField(null=True)
    match_url = models.CharField(max_length=250, null=True)
    game = models.CharField(max_length=250, null=True)
    league = models.CharField(max_length=250, null=True)
    league_img = models.FileField(null=True)
    channel_img = models.FileField(upload_to='channels', null=True)
    channel_title = models.CharField(max_length=250, null=True)
    is_match_details_crawled = models.IntegerField(max_length=4, null=True)
    home_team = models.CharField(max_length=255, null=True)
    away_team = models.CharField(max_length=255, null=True)
    home_team_id = models.CharField(max_length=255, null=True)
    away_team_id = models.CharField(max_length=255, null=True)
    league_id = models.CharField(max_length=250, null=True)
    league_country = models.CharField(max_length=250, null=True)
    match_details_json = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.DateTimeField(null=True)
    status_type = models.CharField(max_length=20, null=True)
    status_short = models.CharField(max_length=10, null=True)
    status_long = models.CharField(max_length=45, null=True)
    round = models.CharField(max_length=100, null=True)
    scores = models.CharField(max_length=10, null=True)
    class Meta:
        indexes = [
            models.Index(fields=("match_unique_id",), name='match_unique_id'),
            models.Index(fields=("parsed_match_date_time",), name='parsed_match_date_time')
        ]

class FootballTeam(models.Model):
    bold_team_id = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    img = models.CharField(max_length=250,null=True)
    team_info = models.JSONField(null=True)
    results = models.JSONField(null=True)
    fixtures = models.JSONField(null=True)
    players = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.DateTimeField(null=True)

class FootballLeague(models.Model):
    league_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    season = models.CharField(max_length=250,null=True)
    league_img = models.CharField(max_length=250,null=True)
    league_standing = models.JSONField(null=True)
    upcoming_matches = models.JSONField(null=True)
    recent_matches = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.DateTimeField(null=True)


class FootballBookmaker(models.Model):
    # match_id = models.IntegerField(max_length=11)
    match = models.ForeignKey(FootballMatch, on_delete=models.CASCADE, db_constraint=False, related_name='bookmakers')
    name = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    img = models.FileField(upload_to='bookmakers', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

