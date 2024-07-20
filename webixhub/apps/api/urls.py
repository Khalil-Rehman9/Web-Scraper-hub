from django.urls import path
from . import views

urlpatterns = [
    path('api/get_league', views.getLeague),
    path('api/get_matches', views.getMatch),
    path('api/get_match_details', views.getMatchDetails),
    path('api/get_team_details', views.getTeamDetails),
    path('api/get_league_details', views.getLeagueDetails),
    path('api/get_league_ids', views.getLatestLeagueIds),
]