from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("assignments/", views.assignments, name="assignments"),
    path("tdl/<int:id>", views.list, name="list"),
    path("courses/", views.courses, name="courses"),
    path("tdl/", views.tdl, name="tdl"),
    path("discuss/", views.discuss, name="discuss"),
    path("discuss/<int:id>", views.discussPost, name="discussPost"),
    path("modules", views.modules, name="modules"),
] 