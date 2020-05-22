from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #path("<name>", views.mainPage, name="main"),
    path("about/", views.about, name="about"),
    #path("contact/", views.contact, name="contact"),
    path("home/", views.home, name="main"),
    path("release/", views.release, name="release"),
    path("home2/", views.home2, name="home2"),
    path("test/", views.get_name, name="test"),
    path('compare/', views.compare, name='compare'),
    path('generate/', views.generate, name='generate'),
]

