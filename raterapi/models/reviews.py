from django.db import models

class Reviews(models.Model):
    game = models.ForeignKey("Games", on_delete=models.CASCADE, related_name="reviews")
    rater = models.ForeignKey("Raters", on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    created_on = models.DateField()