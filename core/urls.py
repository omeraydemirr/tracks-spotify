from django.urls import path
from core import views

urlpatterns = [
    path('tracks/<str:genre>',views.TrackInfo.as_view()),
    path('',views.Search.as_view())
]