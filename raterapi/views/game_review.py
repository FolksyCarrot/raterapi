from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from raterapi.models import Raters, Reviews, Games

class ReviewView(ViewSet):

    def create(self, request):
        rater = Raters.objects.get(user = request.auth.user)
        game = Games.objects.get(pk = request.data["gameId"])

        try: 
            review = Reviews.objects.create(
               game = game,
               rater = rater,
               content = request.data["content"],
               created_on = request.data["createdOn"]
               )
            serializer=ReviewSerializer(review, context = {'request': request})
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            review = Reviews.objects.get(pk=pk)
            serializer=ReviewSerializer(review, context = {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        review = Reviews.objects.all()
        serializer = ReviewSerializer(
        review, many=True, context={'request': request})
        return Response(serializer.data)

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

class ReviewSerializer(serializers.ModelSerializer):
    rater=RaterSerializer()
    game = GameSerializer()
    class Meta:
        model = Reviews
        fields = ('id', 'game', 'rater', 'content', 'created_on')
        depth = 1