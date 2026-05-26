from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

import razorpay

from .forms import SignupForm, CarForm, ProfileForm
from .models import Car, Booking, Wishlist


def is_profile_complete(user):
    return (
        user.email and
        user.phone and
        user.address and
        user.user_type
    )


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.user_type == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if user.user_type == 'seller':
                    return redirect('seller_dashboard')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):

    if request.user.is_authenticated:
        if not is_profile_complete(request.user):
            return redirect('profile')

    cars = Car.objects.filter(is_sold=False).order_by('-created_at')

    brand = request.GET.get('brand')
    fuel = request.GET.get('fuel')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if brand:
        cars = cars.filter(brand__icontains=brand)

    if fuel:
        cars = cars.filter(fuel_type__icontains=fuel)

    if city:
        cars = cars.filter(city__icontains=city)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    return render(request, 'buyer/home.html', {'cars': cars})

@login_required
def buyer_dashboard(request):
    if not is_profile_complete(request.user):
        return redirect('profile')

    return redirect('home')


@login_required
def seller_dashboard(request):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'seller':
        return redirect('home')

    cars = Car.objects.filter(seller=request.user)

    return render(request, 'seller/dashboard.html', {'cars': cars})


@login_required
def add_car(request):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'seller':
        return redirect('home')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.save()

            return redirect('seller_dashboard')
    else:
        form = CarForm()

    return render(request, 'seller/add_car.html', {'form': form})


@login_required(login_url='login')
def car_detail(request, car_id):

    car = Car.objects.get(id=car_id)

    if car.is_sold:
        return redirect('home')

    return render(request, 'buyer/car_detail.html', {'car': car})


@login_required
def edit_car(request, car_id):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'seller':
        return redirect('home')

    car = Car.objects.get(id=car_id, seller=request.user)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = CarForm(instance=car)

    return render(request, 'seller/edit_car.html', {'form': form})


@login_required
def delete_car(request, car_id):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'seller':
        return redirect('home')

    car = Car.objects.get(id=car_id, seller=request.user)
    car.delete()

    return redirect('seller_dashboard')


@login_required
def book_car(request, car_id):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'buyer':
        return redirect('seller_dashboard')

    car = Car.objects.get(id=car_id)
    if car.is_sold:
        return redirect('home')

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        'amount': int(car.booking_amount * 100),
        'currency': 'INR',
        'payment_capture': '1'
    })

    Booking.objects.create(
        buyer=request.user,
        car=car,
        booking_amount=car.booking_amount,
        payment_id=payment['id']
    )

    context = {
        'car': car,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }

    return render(request, 'buyer/payment.html', context)


@login_required
def payment_success(request):
    payment_id = request.GET.get('payment_id')

    booking = Booking.objects.filter(
        payment_id=payment_id
    ).first()

    if booking:
        booking.status = 'Confirmed'
        booking.save()

    return render(request, 'buyer/payment_success.html')


@login_required
def my_bookings(request):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'buyer':
        return redirect('seller_dashboard')

    bookings = Booking.objects.filter(
        buyer=request.user
    ).order_by('-created_at')

    return render(request, 'buyer/my_bookings.html', {'bookings': bookings})


@login_required
def seller_bookings(request):
    if not is_profile_complete(request.user):
        return redirect('profile')

    if request.user.user_type != 'seller':
        return redirect('home')

    bookings = Booking.objects.filter(
        car__seller=request.user
    ).order_by('-created_at')

    return render(request, 'seller/bookings.html', {'bookings': bookings})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            if request.user.user_type == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('home')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


@login_required
def select_role(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        if user_type in ['buyer', 'seller']:
            request.user.user_type = user_type
            request.user.save()

            if user_type == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('home')

    return render(request, 'select_role.html')

@login_required
def update_booking_status(request, booking_id, status):

    if request.user.user_type != 'seller':
        return redirect('home')

    booking = Booking.objects.get(
        id=booking_id,
        car__seller=request.user
    )

    if status in ['Confirmed', 'Rejected']:
        booking.status = status
        booking.save()

    return redirect('seller_bookings')

@login_required
def mark_car_sold(request, car_id):

    if request.user.user_type != 'seller':
        return redirect('home')

    car = Car.objects.get(id=car_id, seller=request.user)
    car.is_sold = True
    car.save()

    return redirect('seller_dashboard')

@login_required
def add_to_wishlist(request, car_id):

    if request.user.user_type != 'buyer':
        return redirect('home')

    car = Car.objects.get(id=car_id)

    Wishlist.objects.get_or_create(
        buyer=request.user,
        car=car
    )

    return redirect('home')

@login_required
def my_wishlist(request):

    wishlist = Wishlist.objects.filter(
        buyer=request.user
    )

    return render(
        request,
        'buyer/wishlist.html',
        {'wishlist': wishlist}
    )
    
@login_required
def remove_wishlist(request, wishlist_id):
    wishlist_item = Wishlist.objects.filter(
        id=wishlist_id,
        buyer=request.user
    ).first()

    if wishlist_item:
        wishlist_item.delete()

    return redirect('my_wishlist')