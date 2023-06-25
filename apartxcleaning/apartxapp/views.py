from django.shortcuts import render, redirect, get_object_or_404
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import UserProfile, Customer, Worker, Order, FreeTime, Photo
from django.shortcuts import render
from geopy.geocoders import Nominatim
from django.conf import settings
import requests
import json
# Create your views here.

def get_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    elif location := geolocator.geocode(address, exactly_one=False):
        # Use the first close match found
        latitude = location[0].latitude
        longitude = location[0].longitude
        return latitude, longitude
    else:
        return None

def Directions(*args, **kwargs):

	lat_a = kwargs.get("lat_a")
	long_a = kwargs.get("long_a")
	lat_b = kwargs.get("lat_b")
	long_b = kwargs.get("long_b")

	origin = f'{lat_a},{long_a}'
	destination = f'{lat_b},{long_b}'

	result = requests.get(
		'https://maps.googleapis.com/maps/api/directions/json?',
		 params={
		 'origin': origin,
		 'destination': destination,
		 "key": settings.GOOGLE_API_KEY
		 })

	directions = result.json()

	if directions["status"] == "OK":

		route = directions["routes"][0]["legs"][0]
		origin = route["start_address"]
		destination = route["end_address"]
		distance = route["distance"]["text"]
		duration = route["duration"]["text"]

		steps = [
			[
				s["distance"]["text"],
				s["duration"]["text"],
				s["html_instructions"],

			]
			for s in route["steps"]]

	return {
		"origin": origin,
		"destination": destination,
		"distance": distance,
		"duration": duration,
		"steps": steps
		}


def map(request):
	lat_a, lat_b, long_a, long_b, directions = '','','','', {}

	if request.method == "POST":
		address1 = request.POST['address1']
		address2 = request.POST['address2']
		coordinates1 = get_coordinates(address1)
		coordinates2 = get_coordinates(address2)

		if coordinates1:
			lat_a, long_a = coordinates1
		if coordinates2:
			lat_b, long_b = coordinates2

		directions = Directions(
			lat_a= lat_a,
			long_a=long_a,
			lat_b = lat_b,
			long_b=long_b
			)

	context = {
	"google_api_key": settings.GOOGLE_API_KEY,
	"lat_a": lat_a,
	"long_a": long_a,
	"lat_b": lat_b,
	"long_b": long_b,
	"origin": f'{lat_a}, {long_a}',
	"destination": f'{lat_b}, {long_b}',
	"directions": directions,

	}
	return render(request, 'map.html', context)

@login_required
def add_order(request):
    if request.method == 'POST':
        time = request.POST['time']
        location = request.POST['location']
        cost = request.POST['cost']
        phone_number = request.POST['phone_number']
        checklist = request.POST['checklist']

        user_profile = UserProfile.objects.get(user=request.user, is_customer=True)
        customer = Customer.objects.get(user=user_profile.user)

        order = Order.objects.create(
            customer=customer,
            time=time,
            location=location,
            cost=cost,
            phone_number=phone_number,
            checklist=checklist
        )
        order.save()

        return redirect('index')
    else:
        return render(request, 'add_order.html')

@login_required
def accept_request(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.userprofile.is_customer and not order.accepted:
        worker_id = request.POST.get('worker_id')  # Get the selected worker's ID from the form
        if worker_id:
            worker = get_object_or_404(Worker, id=worker_id)
            order.accepted = True
            order.worker = worker
            order.save()

    return redirect('index')

@login_required
def send_request(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.userprofile.is_worker and not order.accepted:
        order.requested_by.add(request.user.worker)
        order.save()

    return redirect('index')

@login_required
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.userprofile.is_worker and order.worker.user == request.user:
        if request.method == "POST":
            files = request.FILES.getlist('photoreport')

            for file in files:
                photo = Photo.objects.create(image = file)
                order.photoreport.add(photo)

    context = {'order': order}
    return render(request, 'vieworder.html', context)


@login_required
def completed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orders = Order.objects.all()
    if request.user.userprofile.is_customer:
        if request.method == 'POST':
            rating = int(request.POST.get('rating'))
            order.rating = rating
            order.completed = True
            order.save()

            # Calculate and update the average rating for the worker
            worker = order.worker
            worker_ratings = Order.objects.filter(worker=worker, completed=True).values_list('rating', flat=True)
            avg_rating = sum(worker_ratings) / worker_ratings.count() if worker_ratings else 0
            worker.rating = round(avg_rating, 1)
            worker.save()

    context = {'order': order}
    return redirect('index')

@login_required
def workerprofile(request, worker_id):
    plt.xkcd()

    ages_x = [0, 1, 2, 3, 4, 5, 6, 7]

    py_dev_y = [7, 5, 4, 10, 6, 5, 2, 6]
    worker = get_object_or_404(Worker, id=worker_id)
    worker_ratings = Order.objects.filter(worker=worker, completed=True).values_list('rating', flat=True)
    last_rating = worker_ratings.last()
    for i in range(worker_ratings.count()):
        ages_x.append(len(ages_x) + 1)
        py_dev_y.append(last_rating)

    plt.clf()

    fig_desktop, ax_desktop = plt.subplots(figsize=(8, 6), dpi=80)
    ax_desktop.plot(ages_x, py_dev_y, label='Python')
    ax_desktop.set_xlabel('Дни')
    ax_desktop.set_ylabel('Рейтинг')
    ax_desktop.legend()

    buffer_desktop = BytesIO()
    plt.savefig(buffer_desktop, format='png')
    buffer_desktop.seek(0)
    image_base64_desktop = base64.b64encode(buffer_desktop.getvalue()).decode('utf-8')
    buffer_desktop.close()

    context = {
        'image_base64_desktop': image_base64_desktop,
    }

    return render(request, 'workerprofile.html', context)

@login_required
def add_free_time(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        user = request.user

        free_time = FreeTime.objects.create(
            user=user,
            start_time=start_time,
            end_time=end_time,
        )

        worker = Worker.objects.get(user=user)
        worker.free_times.add(free_time)

        return redirect('index')
    return render(request, 'index.html')

def index(request):
    if request.user.userprofile.is_customer:
        orders = Order.objects.filter(customer=request.user.customer)
        my_orders = []
        pass
    elif request.user.userprofile.is_worker:
        orders = Order.objects.filter(accepted=False).exclude(worker=request.user.worker)
        my_orders = Order.objects.filter(worker__user=request.user)
    else:
        orders = []

    free_times = FreeTime.objects.all()

    context = {
        'orders': orders,
        'myorders': my_orders,
        'free_times': free_times,
    }

    return render(request, 'index.html', context)







# auth
def signupsystem(request):
    if request.method == "GET":
        return render(request, 'signupsystem.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] != request.POST['password2']:
            return render(request, 'signupsystem.html',
                          {'form': UserCreationForm, 'error': 'Passwords don\'t match!'})
        else:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                user_profile = UserProfile.objects.create(user=request.user)
                role = request.POST['iswho']
                if role == 'worker':
                    user_profile.is_worker = True
                    user_profile.is_customer = False
                elif role == 'customer':
                    user_profile.is_customer = True
                    user_profile.is_worker = False
                user_profile.save()


                return redirect('index')
            except IntegrityError:
                return render(request, 'signupsystem.html',
                              {'form': UserCreationForm, 'error': 'Username is already taken!'})


def loginsystem(request):
    if request.method == "GET":
        return render(request, 'loginsystem.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'loginsystem.html',
                          {'form': AuthenticationForm, 'error': 'Неверный логин и/или пароль'})


@login_required
def logoutsystem(request):
    if request.method == "GET":
        logout(request)
        return redirect('loginsystem')
