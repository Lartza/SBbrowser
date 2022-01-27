# SPDX-License-Identifier: AGPL-3.0-or-later
from django.urls import path

from . import views

urlpatterns = [
    path('', views.FilteredSponsortimeListView.as_view(), name='index'),
    path('video/<videoid>/', views.FilteredVideoListView.as_view(), name='video'),
    path('userid/<userid>/', views.FilteredUserIDListView.as_view(), name='userid'),
    path('username/<path:username>/', views.FilteredUsernameListView.as_view(), name='username'),
    path('uuid/<uuid>/', views.FilteredUUIDListView.as_view(), name='uuid'),
]
