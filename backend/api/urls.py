
from django.urls import path
from . views import UserRegisterView,UserLoginView

urlpatterns = [
 path("user_register",UserRegisterView.as_view(),name="user_register"),
 path("user_register",UserLoginView.as_view(),name="user_login"),

]