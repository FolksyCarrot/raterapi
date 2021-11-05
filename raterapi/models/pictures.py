from django.db import models

class Picture(models.Model):
    rater = models.ForeignKey("Raters", on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=50)