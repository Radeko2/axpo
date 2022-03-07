from .models import Car,Review
from .serializers import CarSerializer, ReviewSerializer, PopularCarSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
import requests

# Create your views here.


def is_car_valid(make_to_check: str, model_to_check: str):
    make_to_check = make_to_check.upper()
    url2 = "https://vpic.nhtsa.dot.gov/api//vehicles/GetAllMakes?format=json"
    resp = requests.get(url2)
    makes = resp.json().get("Results")
    for make in makes:
        if make.get("Make_Name") == make_to_check:
            make_to_check_id = make.get("Make_ID")
            break
    else:
        return False

    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/{make_to_check_id}?format=json"
    resp = requests.get(url)
    models = resp.json().get("Results")
    for model in models:
        if model.get("Model_Name") == model_to_check:
            return True
    return False


@api_view(["GET", "POST", "DELETE"])
def cars(request, pk=None):
    if request.method == 'GET':
        cars_list = Car.objects.all()
        serializer = CarSerializer(cars_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')

    if request.method == "POST":
        model = request.data.get("model")
        make = request.data.get("make")
        if model and make and is_car_valid(make, model) and not Car.objects.filter(model=model, make=make):
            serializer = CarSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

    if request.method == "DELETE":
        try:
            car = Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        car.delete()
        return Response(status=status.HTTP_202_ACCEPTED, content_type='application/json')


@api_view(["POST"])
def rate(request):
    car_id = request.data.get("car_id")
    rating = request.data.get("rating")
    if car_id and rating and Car.objects.filter(id=car_id).exists():
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


@api_view(["GET"])
def popular(request):
    cars = Car.objects.annotate(total=Count('reviews')).order_by('-total')[:4]
    serializer = PopularCarSerializer(cars, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')




