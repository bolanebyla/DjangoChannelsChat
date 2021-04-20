from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserChatsListView.as_view(), name='index'),
    path('<int:room_id>/', views.room, name='room'),
]
