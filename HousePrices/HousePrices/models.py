from django.db import models

class HousePrediction(models.Model):
    avg_area_income = models.FloatField()
    avg_house_age = models.FloatField()
    avg_area_rooms = models.FloatField()
    avg_area_bedrooms = models.FloatField()
    avg_area_population = models.FloatField()
    predicted_price = models.FloatField()