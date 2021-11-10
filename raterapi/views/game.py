from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterapi.models import Games, Raters, games, Reviews

class GameView(ViewSet):

    def create(self, request):
        rater = Raters.objects.get(user=request.auth.user)
        
        try: 
            game = Games.objects.create(
                rater = rater,
                title = request.data["title"],
                description = request.data["description"],
                designer = request.data["designer"],
                year_released = request.data["yearReleased"],
                number_of_players = request.data["numberOfPlayers"],
                estimated_time_to_play = request.data["estimatedTimeToPlay"],
                age_recommendation = request.data["ageRecommendation"],
                created_on = request.data["createdOn"]
            )
            #serilizer purpose is to bring back only specific info of an object. If you want the entire object values, serilaizer isn't needed

            serializer = GameSerializer(game, context = {'request': request})
            return Response("sure")

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            game = Games.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        games = Games.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reviews
        fields = ('content', 'created_on')

class GameSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, required = False)
    class Meta:
        model = Games
        fields = ('id', 'title', 'description', 'designer', 'year_released', 'number_of_players', 'estimated_time_to_play', 'age_recommendation', 'created_on', 'reviews')
        depth = 1
