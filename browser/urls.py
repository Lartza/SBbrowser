from django.urls import path

from . import views

urlpatterns = [
    path('', views.FilteredSponsortimeListView.as_view(), name='index'),
    path('video/<videoid>/', views.FilteredVideoListView.as_view(), name='video'),
    path('userid/<userid>/', views.FilteredUserIDListView.as_view(), name='userid'),
    path('username/<username>/', views.FilteredUsernameListView.as_view(), name='username'),
]