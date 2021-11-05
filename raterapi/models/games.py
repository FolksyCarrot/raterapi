from django.db import models

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
    
    