from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id, post_request
from .models import CarModel
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.META['HTTP_REFERER'])
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html')
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name =request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New User")

        if not user_exist:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Username already exists"
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {
            "dealerships" :  get_dealers_from_cf(),
        }
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):

    if request.method == "GET":
        context = {
            "dealer": get_dealer_by_id(dealer_id),
            "reviews": get_dealer_reviews_from_cf(dealer_id=dealer_id),
            "cars": CarModel.objects.filter(dealer_id=dealer_id),
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review

def add_review(request, dealer_id):
    
    if request.method == "POST" and request.user.is_authenticated:
        
        car = CarModel.objects.get(pk=request.POST["car"])

        review = {
            "time": datetime.utcnow().isoformat(),
            "dealership": dealer_id,
            "review": request.POST['content'],
            "name": request.user.username,
            "purchase": False,
            "car_make": car.carmake.name,
            "car_model": car.name,
            "car_year": int(car.year.strftime("%Y")),
        }

        post_request(review)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
