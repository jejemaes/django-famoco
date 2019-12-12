from django.urls import path
from . import views

urlpatterns = [
    path('applications', views.api_list, name="api_list"),
    path('add', views.APIApplicationAdd.as_view(), name="api_add")
]
