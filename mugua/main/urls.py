from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("discuss/", views.discuss, name="discuss"),
    path("create/", views.create, name="create"),
    path("view/", views.view, name="view")
] 