from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib import messages
from .models import Car, CartItem, Favorite, TradeOffer, Notification, Offer
from .forms import UserRegisterForm, CarListingForm, TradeOfferForm, OfferForm, UserUpdateForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def index(request):
    featured_cars = Car.objects.all()[:6]
    return render(request, 'index.html', {'featured_cars': featured_cars})

@login_required
def cars_list(request):
    # Get filter parameters
    make = request.GET.get('make')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    sort = request.GET.get('sort')
    
    # Start with all cars
    cars = Car.objects.all()
    
    # Apply filters
    if make:
        cars = cars.filter(make=make)
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)
        
    # Apply sorting
    if sort == 'price_low':
        cars = cars.order_by('price')
    elif sort == 'price_high':
        cars = cars.order_by('-price')
    elif sort == 'year_new':
        cars = cars.order_by('-year')
    elif sort == 'year_old':
        cars = cars.order_by('year')
    
    # Get unique makes for filter dropdown
    makes = Car.objects.values_list('make', flat=True).distinct()
    
    # Get user's favorite cars
    if request.user.is_authenticated:
        favorite_cars = Car.objects.filter(favorites__user=request.user)
    else:
        favorite_cars = []
    
    context = {
        'cars': cars,
        'makes': makes,
        'current_make': make,
        'current_sort': sort,
        'favorite_cars': favorite_cars,
    }
    
    return render(request, 'cars/cars_list.html', context)

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    favorite_cars = []
    
    if request.user.is_authenticated:
        favorite_cars = Car.objects.filter(favorites__user=request.user)
    
    context = {
        'car': car,
        'title': f'{car.year} {car.make} {car.model}',
        'favorite_cars': favorite_cars,
    }
    
    return render(request, 'car_detail.html', context)

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_id=product_id,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart') 

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'register': True}) 

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def form_invalid(self, form):
        # Add this to see login errors
        messages.error(self.request, f'Login failed. Please check your credentials.')
        print(f"Login form errors: {form.errors}")  # This will print to console
        return super().form_invalid(form)
    
    def form_valid(self, form):
        # Add this to confirm successful login
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        print(f"Successful login for user: {self.request.user.username}")  # This will print to console
        return response
    
    def get_success_url(self):
        return reverse_lazy('cars')  # Make sure this matches your URL name
    
    def form_valid(self, form):
        # Add this to ensure proper login
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response 

@login_required
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user
    })

@login_required
def favorites(request):
    # Get the favorite cars for the current user
    favorite_cars = Car.objects.filter(favorites__user=request.user)
    return render(request, 'favorites.html', {
        'favorite_cars': favorite_cars
    })

@login_required
def add_to_favorites(request, car_id):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=car_id)
        Favorite.objects.get_or_create(user=request.user, car=car)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def remove_from_favorites(request, car_id):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=car_id)
        Favorite.objects.filter(user=request.user, car=car).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def history(request):
    # You can track viewed cars here
    return render(request, 'history.html') 

@login_required
def list_car(request):
    if request.method == 'POST':
        form = CarListingForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            messages.success(request, 'Your car has been listed successfully!')
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarListingForm()
    
    return render(request, 'cars/list_car.html', {'form': form})

@login_required
def make_trade_offer(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if car.owner == request.user:
        messages.error(request, "You cannot make a trade offer on your own car.")
        return redirect('car_detail', car_id=car_id)
    
    if request.method == 'POST':
        form = TradeOfferForm(request.user, request.POST)
        if form.is_valid():
            trade_offer = form.save(commit=False)
            trade_offer.buyer = request.user
            trade_offer.seller_car = car
            trade_offer.save()

            # Create notification for the car owner
            Notification.objects.create(
                recipient=car.owner,
                notification_type='trade_offer',
                trade_offer=trade_offer,
                message=f"{request.user.username} has proposed a trade for your {car.year} {car.make} {car.model}"
            )

            messages.success(request, 'Your trade offer has been submitted!')
            return redirect('car_detail', car_id=car_id)
    else:
        form = TradeOfferForm(request.user)
    
    return render(request, 'cars/trade_offer.html', {
        'form': form,
        'car': car
    })

@login_required
def trade_offers(request):
    # Get offers received and made by the user
    received_offers = TradeOffer.objects.filter(seller_car__owner=request.user)
    made_offers = TradeOffer.objects.filter(buyer=request.user)
    
    return render(request, 'cars/trade_offers.html', {
        'received_offers': received_offers,
        'made_offers': made_offers
    })

@login_required
def handle_trade_offer(request, offer_id, action):
    offer = get_object_or_404(TradeOffer, id=offer_id)
    
    
    if offer.seller_car.owner != request.user:
        messages.error(request, "You don't have permission to handle this offer.")
        return redirect('trade_offers')
    
    notification_message = ""
    
    if action == 'accept':
        offer.status = 'accepted'
        notification_message = (
            f"Your trade offer for {offer.seller_car.year} {offer.seller_car.make} {offer.seller_car.model} "
            f"has been accepted by {request.user.username}."
        )
        messages.success(request, 'Trade offer accepted!')
    
    elif action == 'reject':
        offer.status = 'rejected'
        notification_message = (
            f"Your trade offer for {offer.seller_car.year} {offer.seller_car.make} {offer.seller_car.model} "
            f"has been rejected by {request.user.username}."
        )
        messages.info(request, 'Trade offer rejected.')
    
    offer.save()
    
    
    Notification.objects.create(
        recipient=offer.buyer,
        notification_type=f'trade_offer_{offer.status}',  
        trade_offer=offer,
        message=notification_message
    )
    
    return redirect('trade_offers')


@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def make_offer(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if car.owner == request.user:
        messages.error(request, "You cannot make an offer on your own car.")
        return redirect('car_detail', car_id=car_id)
    
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.buyer = request.user
            offer.car = car
            offer.save()

            # Create notification for the car owner
            Notification.objects.create(
                recipient=car.owner,
                notification_type='offer_received',
                offer=offer,
                message=f"{request.user.username} has made an offer of ${offer.amount} for your {car.year} {car.make} {car.model}"
            )

            messages.success(request, 'Your offer has been submitted!')
            return redirect('car_detail', car_id=car_id)
    else:
        form = OfferForm()
    
    return render(request, 'cars/make_offer.html', {
        'form': form,
        'car': car
    })

@login_required
def view_offers(request):
    # Get offers received for user's cars (seller view)
    offers = Offer.objects.filter(car__owner=request.user)
    return render(request, 'cars/seller_offers.html', {'offers': offers})

@login_required
def handle_offer(request, offer_id, action):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    offer = get_object_or_404(Offer, id=offer_id)
    
    # Check permissions
    is_seller = offer.car.owner == request.user
    is_buyer = offer.buyer == request.user
    
    if not (is_seller or is_buyer):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    try:
        message = ''
        notification_type = ''
        
        if action == 'accept':
            offer.status = 'accepted'
            message = 'Offer accepted!'
            notification_type = 'offer_accepted'
            
            # Create notification for buyer
            Notification.objects.create(
                recipient=offer.buyer,
                notification_type=notification_type,
                offer=offer,
                message=f"Great news! Your offer of ${offer.amount:,.2f} for the {offer.car.year} {offer.car.make} {offer.car.model} has been accepted. You can now contact the seller."
            )
        elif action == 'reject':
            offer.status = 'rejected'
            message = 'Offer rejected.'
            notification_type = 'offer_rejected'
            
            # Create notification for buyer
            Notification.objects.create(
                recipient=offer.buyer,
                notification_type=notification_type,
                offer=offer,
                message=f"Your offer of ${offer.amount:,.2f} for the {offer.car.year} {offer.car.make} {offer.car.model} has been rejected."
            )
        
        offer.save()
        return JsonResponse({'status': 'success', 'message': message})
        
    except Exception as e:
        print(f"Error in handle_offer: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def my_offers(request):
    # Get offers made by the user (buyer view)
    made_offers = Offer.objects.filter(buyer=request.user)
    
    # Debug print
    for offer in made_offers:
        print(f"Offer {offer.id} status: {offer.status}")
    
    return render(request, 'cars/my_offers.html', {'made_offers': made_offers})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'cars/edit_profile.html', {
        'form': form
    })