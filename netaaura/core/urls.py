from django.urls import path
from . import views

urlpatterns = [
    # Public / user URLs
    path("", views.politician_list, name="politician_list"),
    path("politicians/add/", views.add_politician, name="add_politician"),
    path("politicians/<int:pk>/", views.politician_detail, name="politician_detail"),
    path("politicians/<int:pk>/rate/", views.rate_politician, name="rate_politician"),

    # Admin-only URLs
    path("approve/", views.approve_politicians_view, name="approve_politicians"),
    path("approve/<int:pk>/", views.approve_politician_action, name="approve_politician"),
    path("politician/<int:pk>/delete/", views.delete_politician, name="delete_politician"),
]
