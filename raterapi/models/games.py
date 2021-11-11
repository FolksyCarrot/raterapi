from django.db import models
from raterapi.models import GameRating

class Games(models.Model):
    rater = models.ForeignKey("Raters", on_delete=models.CASCADE)
    title = models. CharField(max_length=50)
    description = models. CharField(max_length=50)
    designer = models. CharField(max_length=50)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.IntegerField()
    age_recommendation = models.IntegerField()
    created_on = models.DateField()
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        try:
            ratings = GameRating.objects.filter(game=self)

        # Sum all of the ratings for the game
            total_rating = 0
            for rating in ratings:
                total_rating += rating.rating

            return total_rating/len(ratings)

        except:
            return 'game has no rating'
        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.
