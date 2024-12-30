from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars_list, name='cars'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.history, name='history'),
    path('favorites/add/<int:car_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:car_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('list-car/', views.list_car, name='list_car'),
    path('trade-offer/<int:car_id>/', views.make_trade_offer, name='make_trade_offer'),
    path('trade-offers/', views.trade_offers, name='trade_offers'),
    path('trade-offer/<int:offer_id>/<str:action>/', views.handle_trade_offer, name='handle_trade_offer'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('car/<int:car_id>/offer/', views.make_offer, name='make_offer'),
    path('offers/', views.view_offers, name='view_offers'),
    path('offers/<int:offer_id>/<str:action>/', views.handle_offer, name='handle_offer'),
    path('my-offers/', views.my_offers, name='my_offers'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
] 