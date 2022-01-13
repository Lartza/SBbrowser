# SPDX-License-Identifier: AGPL-3.0-or-later
from django.urls import path

from ratelimit.decorators import ratelimit

from . import views

urlpatterns = [
    path('', ratelimit(key='ip', rate='5/m', block=True)(views.FilteredSponsortimeListView.as_view()), name='index'),
    path('video/<videoid>/', views.FilteredVideoListView.as_view(), name='video'),
    path('userid/<userid>/', views.FilteredUserIDListView.as_view(), name='userid'),
    path('username/<path:username>/', views.FilteredUsernameListView.as_view(), name='username'),
]
