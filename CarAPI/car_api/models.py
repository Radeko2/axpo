from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count

# Create your models here.


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.make}_{self.model}"

    @property
    def avg_rating(self):
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg_rating:
            return round(avg_rating, 1)
        return avg_rating

    @property
    def rates_number(self):
        return self.reviews.aggregate(rates_number=Count('rating'))['rates_number']


class Review(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Review of {self.car_id.make}_{self.car_id.model}"
