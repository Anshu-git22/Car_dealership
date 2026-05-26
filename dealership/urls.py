from django.urls import path
from . import views

urlpatterns = [

     path('', views.home, name='home'),
    
    path('signup/', views.signup_view, name='signup'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),

    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    
    path('seller/add-car/', views.add_car, name='add_car'),
    
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    
    path('seller/edit-car/<int:car_id>/', views.edit_car, name='edit_car'),
    
    path('seller/delete-car/<int:car_id>/', views.delete_car, name='delete_car'),
    
    path('book-car/<int:car_id>/', views.book_car, name='book_car'),
    
    path('payment-success/',views.payment_success, name='payment_success'),
    
    path('my-bookings/',views.my_bookings,name='my_bookings'),
    
    path('seller/bookings/',views.seller_bookings,name='seller_bookings'),
    
    path('profile/', views.profile_view, name='profile'),
    
    path('select-role/', views.select_role, name='select_role'),
    
    path(
    'seller/booking/<int:booking_id>/<str:status>/',
    views.update_booking_status,
    name='update_booking_status'
),
    
    path('seller/car/<int:car_id>/sold/', views.mark_car_sold, name='mark_car_sold'),
    
    path(
    'wishlist/add/<int:car_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),

path(
    'my-wishlist/',
    views.my_wishlist,
    name='my_wishlist'
),

path(
    'wishlist/remove/<int:wishlist_id>/',
    views.remove_wishlist,
    name='remove_wishlist'
),
]