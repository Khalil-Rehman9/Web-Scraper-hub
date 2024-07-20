import datetime

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..sports.models import FootballMatch, FootballTeam, FootballLeague
from .serializers import MatchSerializer, LeagueSerializer, TeamSerializer, LeagueListSerializer


@api_view(['GET'])
def getLeague(request):
    matches = FootballMatch.objects.values('league').distinct()
    serializer = LeagueListSerializer(matches,many=True,fields=['league'])
    response_value = {
     'status': 'success',
     'data': serializer.data
    }
    return Response(response_value)

@api_view(['GET'])
def getMatch(request):
    league = request.GET.get('league')
    today = datetime.datetime.today()
    if league:
        matches = FootballMatch.objects.filter(parsed_match_date_time__gte=today, is_match_details_crawled__exact='1').filter(league=league)
    else:
        matches = FootballMatch.objects.filter(parsed_match_date_time__date__gte=today.date(), is_match_details_crawled__exact='1').all().order_by('parsed_match_date_time')
    context = {'request': request}
    serializer = MatchSerializer(matches, fields=['id', 'match_date', 'match_time', 'parsed_match_date_time', 'game', 'league', 'home_team', 'away_team', 'league_img', 'channel_img', 'channel_title', 'match_unique_id', 'bookmakers'], many=True, context=context)
    response_value = {
        'status': 'success',
        'data': serializer.data
    }
    return Response(response_value)

@api_view(['GET'])
def getMatchDetails(request):
    match_id = request.GET.get('match_id')
    match_details = FootballMatch.objects.get(id=match_id)
    context = {'request': request}
    serializer = MatchSerializer(match_details, fields=['id', 'match_date', 'match_time', 'parsed_match_date_time', 'game', 'league',  'league_id', 'league_img', 'channel_img', 'channel_title', 'match_unique_id', 'bookmakers', 'away_team',  'home_team', 'away_team_id',  'home_team_id', 'match_details_json', 'status_type', 'status_short', 'status_long', 'round', 'scores'], many=False, context=context)
    tv_names = {
        'tv3sport': 'TV 3 sport',
        'tv2sport': 'TV 2 sport',
        'tv2sportx': 'TV 2 sportx',
        '6763': 'TV3 MAX',
        'canal9': 'Canal 9',
        '6eren': '6 Eren',
        'tv3plus_2': 'TV 3 plus 2',
        'dr2': 'DR2',
        'tv2': 'TV2',
        'see': 'SEE',
    }
    response_value = {
        'status': 'success',
        'tv_names': tv_names,
        'data': serializer.data
    }
    return Response(response_value)

@api_view(['GET'])
def getTeamDetails(request):
    team_id = request.GET.get('team_id')
    team_details = FootballTeam.objects.get(bold_team_id=team_id)
    context = {'request': request}
    team_data = TeamSerializer(team_details, fields=['id', 'bold_team_id', 'name', 'img', 'team_info', 'results', 'fixtures', 'players'], many=False, context=context)
    upcoming_matches = FootballMatch.objects.raw('''SELECT 
                                                        sports_footballmatch.id,
                                                        parsed_match_date_time,
                                                        league,
                                                        match_time,
	                                                    match_date,
                                                        league_id,
                                                        home_team,
                                                        away_team,
                                                        home_team.img as home_team_img,
                                                        away_team.img as away_team_img
                                                    FROM webixhub.sports_footballmatch
                                                    LEFT JOIN sports_footballteam as home_team on home_team.bold_team_id = home_team_id
                                                    LEFT JOIN sports_footballteam as away_team on away_team.bold_team_id = away_team_id
                                                        WHERE parsed_match_date_time > NOW()
                                                        AND (home_team_id = %s OR away_team_id = %s)  ORDER BY parsed_match_date_time ASC LIMIT 5''', [team_id, team_id])
    upcoming_matches = MatchSerializer(upcoming_matches,
                                       fields=['id', 'parsed_match_date_time', 'league', 'league_id', 'home_team',
                                               'away_team', 'home_team_img', 'away_team_img', 'match_date', 'match_time'], many=True, context=context)
    previous_matches = FootballMatch.objects.raw('''SELECT 
                                                        sports_footballmatch.id,
                                                        parsed_match_date_time,
                                                        league,
                                                        match_time,
	                                                    match_date,
                                                        league_id,
                                                        home_team,
                                                        away_team,
                                                        home_team.img as home_team_img,
                                                        away_team.img as away_team_img,
                                                        status_type, status_short, status_long, round, scores
                                                    FROM webixhub.sports_footballmatch
                                                    LEFT JOIN sports_footballteam as home_team on home_team.bold_team_id = home_team_id
                                                    LEFT JOIN sports_footballteam as away_team on away_team.bold_team_id = away_team_id
                                                        WHERE parsed_match_date_time < NOW()
                                                        AND (home_team_id = %s OR away_team_id = %s) ORDER BY parsed_match_date_time DESC LIMIT 5''', [team_id, team_id])
    previous_matches = MatchSerializer(previous_matches, fields=['id', 'parsed_match_date_time', 'league', 'league_id', 'home_team', 'away_team', 'home_team_img', 'away_team_img', 'match_date', 'match_time', 'status_type', 'status_short', 'status_long', 'round', 'scores'], many=True, context=context)
    response_value = {
        'status': 'success',
        'data': {
            'team_data': team_data.data,
            'upcoming_matches': upcoming_matches.data,
            'previous_matches': previous_matches.data
        }
    }
    return Response(response_value)

@api_view(['GET'])
def getLatestLeagueIds(request):
    today = datetime.datetime.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=30)
    matches = FootballMatch.objects.filter(parsed_match_date_time__date__gte=last_month.date()).values('league_id', 'league', 'league_country').distinct()
    serializer = LeagueListSerializer(matches, many=True, fields=['league_id', 'league', 'league_country'])
    response_value = {
     'status': 'success',
     'data': serializer.data
    }
    return Response(response_value)


@api_view(['GET'])
def getLeagueDetails(request):
    league_id = request.GET.get('league_id')
    try:
        league_details = FootballLeague.objects.filter(league_id=league_id).order_by('-id')[0]
    except FootballLeague.DoesNotExist:
        league_details = None
    context = {'request': request}
    league_standing = LeagueSerializer(league_details, fields=['id', 'league_id', 'name', 'name', 'season', 'league_img', 'league_standing', 'upcoming_matches', 'recent_matches'], many=False, context=context)
    upcoming_matches = FootballMatch.objects.raw('''SELECT 
                                                            sports_footballmatch.id,
                                                            parsed_match_date_time,
                                                            league,
                                                            match_time,
    	                                                    match_date,
                                                            league_id,
                                                            home_team,
                                                            away_team,
                                                            home_team.img as home_team_img,
                                                            away_team.img as away_team_img
                                                        FROM webixhub.sports_footballmatch
                                                        LEFT JOIN sports_footballteam as home_team on home_team.bold_team_id = home_team_id
                                                        LEFT JOIN sports_footballteam as away_team on away_team.bold_team_id = away_team_id
                                                            WHERE parsed_match_date_time > NOW()
                                                            AND (league_id = %s)  ORDER BY parsed_match_date_time ASC LIMIT 10''',
                                                 [league_id])
    upcoming_matches = MatchSerializer(upcoming_matches,
                                       fields=['id', 'parsed_match_date_time', 'league', 'league_id', 'home_team',
                                               'away_team', 'home_team_img', 'away_team_img', 'match_date',
                                               'match_time'], many=True, context=context)
    previous_matches = FootballMatch.objects.raw('''SELECT 
                                                            sports_footballmatch.id,
                                                            parsed_match_date_time,
                                                            league,
                                                            match_time,
    	                                                    match_date,
                                                            league_id,
                                                            home_team,
                                                            away_team,
                                                            home_team.img as home_team_img,
                                                            away_team.img as away_team_img
                                                        FROM webixhub.sports_footballmatch
                                                        LEFT JOIN sports_footballteam as home_team on home_team.bold_team_id = home_team_id
                                                        LEFT JOIN sports_footballteam as away_team on away_team.bold_team_id = away_team_id
                                                            WHERE parsed_match_date_time < NOW()
                                                            AND (league_id = %s) ORDER BY parsed_match_date_time DESC LIMIT 10''',
                                                 [league_id])
    previous_matches = MatchSerializer(previous_matches,
                                       fields=['id', 'parsed_match_date_time', 'league', 'league_id', 'home_team',
                                               'away_team', 'home_team_img', 'away_team_img', 'match_date',
                                               'match_time'], many=True, context=context)
    league_img = FootballMatch.objects.raw('''SELECT id, league_img FROM webixhub.sports_footballmatch WHERE (league_id = %s) ORDER BY parsed_match_date_time DESC LIMIT 1''',[league_id])
    league_img = MatchSerializer(league_img,
                                       fields=['id', 'league_img'], many=True, context=context)
    response_value = {
        'status': 'success',
        'data': {
            'league_standing': league_standing.data,
            'upcoming_matches': upcoming_matches.data,
            'previous_matches': previous_matches.data,
            'league_img': league_img.data
        }
    }
    return Response(response_value)
