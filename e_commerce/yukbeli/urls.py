from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path("account/", include("django.contrib.auth.urls")),
    path('logout/', views.logout_request, name="logout"),


]