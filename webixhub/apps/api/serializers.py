from rest_framework import serializers

from ..sports.models import FootballMatch, FootballBookmaker, FootballTeam, FootballLeague
from .dynamic_fields_model_serializer import DynamicFieldsModelSerializer


class LeagueSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = FootballLeague
        fields = '__all__'

class LeagueListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = FootballMatch
        fields = '__all__'

class BookmakersSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = FootballBookmaker
        fields = '__all__'

class MatchSerializer(DynamicFieldsModelSerializer):
    bookmakers = BookmakersSerializer(read_only=True, many=True)
    league_img = serializers.SerializerMethodField('get_league_img')
    channel_img = serializers.SerializerMethodField('get_channel_img')
    home_team_img = serializers.SerializerMethodField()
    away_team_img = serializers.SerializerMethodField()

    def get_league_img(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.league_img.url)

    def get_channel_img(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.channel_img.url)

    def get_home_team_img(self, obj):
        return {
            'home_team_img': obj.home_team_img,
        }

    def get_away_team_img(self, obj):
        return {
            'away_team_img': obj.away_team_img,
        }

    class Meta:
        model = FootballMatch
        fields = '__all__'

class TeamSerializer(DynamicFieldsModelSerializer):
    img = serializers.SerializerMethodField('get_img')

    def get_img(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.img)

    class Meta:
        model = FootballTeam
        fields = '__all__'