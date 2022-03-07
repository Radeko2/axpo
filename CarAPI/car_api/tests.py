from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Car, Review


class TestCarsAPI(APITestCase):
    valid_make = "Audi"
    valid_model = "A4"
    invalid_make = "AAA"
    invalid_model = "BBB"
    valid_car = {"make": valid_make, "model": valid_model}
    invalid_car = {"make": invalid_make, "model": invalid_model}

    def test_cars_post_positive(self):
        previous_car_count = Car.objects.all().count()
        valid_car = {"make": self.valid_make, "model": self.valid_model}
        resp = self.client.post(reverse('cars'), valid_car)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.all().count(), previous_car_count+1)
        self.assertEqual(resp.data.get("make"), self.valid_make)
        self.assertEqual(resp.data.get("model"), self.valid_model)

    def test_cars_post_negative(self):
        previous_car_count = Car.objects.all().count()
        resp = self.client.post(reverse('cars'), self.invalid_car)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Car.objects.all().count(), previous_car_count)

    def test_cars_get(self):
        car = Car(**self.valid_car)
        car.save()
        resp = self.client.get(reverse('cars'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data[0]["make"], self.valid_make)
        self.assertEqual(resp.data[0]["model"], self.valid_model)

    def test_car_delete_positive(self):
        car = Car(**self.valid_car)
        car.save()
        previous_car_count = Car.objects.all().count()
        resp = self.client.delete(reverse('del_cars', args=[1]))
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Car.objects.all().count(), previous_car_count-1)

    def test_car_delete_negative(self):
        car = Car(**self.valid_car)
        car.save()
        previous_car_count = Car.objects.all().count()
        resp = self.client.delete(reverse('del_cars', args=[2]))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Car.objects.all().count(), previous_car_count)


class TestRateAPI(APITestCase):
    valid_make = "Audi"
    valid_model = "A4"
    valid_car = {"make": valid_make, "model": valid_model}
    valid_rating = 1
    invalid_rating = 6

    def test_rate_positive(self):
        car = Car(**self.valid_car)
        car.save()
        previous_review_count = Review.objects.filter(car_id=car.id).count()
        valid_review = {"car_id": 1, "rating": self.valid_rating}
        resp = self.client.post(reverse("rate"),valid_review)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.filter(car_id=car.id).count(), previous_review_count + 1)

    def test_rate_negative(self):
        car = Car(**self.valid_car)
        car.save()
        previous_review_count = Review.objects.filter(car_id=car.id).count()
        valid_review = {"car_id": 1, "rating": self.invalid_rating}
        resp = self.client.post(reverse("rate"),valid_review)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.filter(car_id=car.id).count(), previous_review_count)


class TestPopularAPI(APITestCase):

    def test_popular(self):
        car1 = Car(model="A4", make="Audi")
        car1.save()
        car2 = Car(model="DB9", make="ASTON MARTIN")
        car2.save()
        review1 = Review(car_id=car1, rating=5)
        review1.save()
        review2 = Review(car_id=car2, rating=1)
        review2.save()
        review3 = Review(car_id=car2, rating=1)
        review3.save()
        resp = self.client.get(reverse("popular"))
        self.assertEqual(resp.status_code,status.HTTP_200_OK)
        self.assertEqual(resp.data[0]["make"], "ASTON MARTIN")
        self.assertEqual(resp.data[0]["model"], "DB9")
        self.assertEqual(resp.data[1]["make"], "Audi")
        self.assertEqual(resp.data[1]["model"], "A4")









