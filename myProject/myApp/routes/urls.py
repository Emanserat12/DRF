from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from myApp.apis.user import UserDetails, UserCurd
from myApp.apis.order import OrderDetails
from myApp.apis.products import ProductClass

router = routers.SimpleRouter()
router.register(r'order', OrderDetails, basename="order")
router.register(r'users', UserDetails, basename="users")

app_name = 'myApp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductClass.as_view(), name="products"),
    path('products/<str:pk>/', ProductClass.as_view(), name="products"),
    path('users/<int:pk>/', UserCurd.as_view(), name="user_get_or_update"),
    path('', include(router.urls)),
]
