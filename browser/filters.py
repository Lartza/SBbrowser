# SPDX-License-Identifier: AGPL-3.0-or-later
from django_filters import FilterSet, CharFilter, AllValuesFilter, AllValuesMultipleFilter, RangeFilter
from django_filters.widgets import RangeWidget

from .models import Sponsortime

FIELDS = ['videoid', 'votes', 'views', 'category', 'shadowhidden', 'uuid', 'username', 'user']


class UserIDFilter(FilterSet):
    votes = RangeFilter(widget=RangeWidget(attrs={'type': 'number', 'step': 1}))
    views = RangeFilter(widget=RangeWidget(attrs={'type': 'number', 'step': 1}))
    category = AllValuesMultipleFilter()
    shadowhidden = AllValuesFilter(empty_label='Shadowhidden')

    class Meta:
        model = Sponsortime
        fields = FIELDS
        exclude = ['username', 'user']


class UsernameFilter(UserIDFilter):
    user = CharFilter()

    class Meta:
        model = Sponsortime
        fields = FIELDS
        exclude = 'username'


class SponsortimeFilter(UsernameFilter):
    username = CharFilter(field_name='user__username', label='Username')

    class Meta:
        model = Sponsortime
        fields = FIELDS


class VideoFilter(SponsortimeFilter):
    class Meta:
        model = Sponsortime
        fields = FIELDS
        exclude = 'videoid'
