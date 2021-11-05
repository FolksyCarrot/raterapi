from django.db import models

class GameRating(models.Model):
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    rater = models.ForeignKey("Raters", on_delete=models.CASCADE)
    rating = models.IntegerField()