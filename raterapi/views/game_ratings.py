from django.core.exceptions import ValidationError
from django.db.models import fields
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from raterapi.models import GameRating, Raters, Games, gameRatings

class RatingsView(ViewSet):
    def create(self, request):
        rater = Raters.objects.get(user = request.auth.user)
        game = Games.objects.get(pk = request.data["game_id"])

        rating = GameRating.objects.create(
            game = game,
            rater = rater,
            rating = request.data['rating']
        )

        serializer=RatingSerializer(rating, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def list(self, request):
        rating = GameRating.objects.all()
        serializer=RatingSerializer(rating, many=True, context = {'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        rating = GameRating.objects.get(pk=pk)
        serializer=RatingSerializer(rating, context = {'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ('title', 'description')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class RaterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Raters
        fields = ('id', 'user')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRating
        fields = ('id','rating')