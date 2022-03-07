from rest_framework import serializers
from .models import Car, Review


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, obj):
        return obj.avg_rating

    class Meta:
        model = Car
        fields = ['id', 'model', 'make', 'avg_rating']


class PopularCarSerializer(serializers.ModelSerializer):
    rates_number = serializers.SerializerMethodField()

    def get_rates_number(self, obj):
        return obj.rates_number

    class Meta:
        model = Car
        fields = ['id', 'model', 'make', 'rates_number']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['car_id', 'rating']
