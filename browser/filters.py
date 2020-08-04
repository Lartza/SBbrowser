from django_filters import FilterSet, CharFilter, NumberFilter, AllValuesFilter, AllValuesMultipleFilter

from .models import Sponsortime


class SponsortimeFilter(FilterSet):
    votes__gt = NumberFilter(field_name='votes', lookup_expr='gt')
    votes__lt = NumberFilter(field_name='votes', lookup_expr='lt')
    views__gt = NumberFilter(field_name='views', lookup_expr='gt')
    views__lt = NumberFilter(field_name='views', lookup_expr='lt')
    category = AllValuesMultipleFilter()
    hidden = AllValuesFilter(field_name='shadowhidden', empty_label='Shadowhidden')
    username = CharFilter(field_name='user__username', label='Username')
    user = CharFilter()

    class Meta:
        model = Sponsortime
        fields = ['videoid', 'votes__gt', 'votes__lt', 'views__gt', 'views__lt', 'category', 'hidden', 'uuid']


class VideoFilter(FilterSet):
    votes__gt = NumberFilter(field_name='votes', lookup_expr='gt')
    votes__lt = NumberFilter(field_name='votes', lookup_expr='lt')
    views__gt = NumberFilter(field_name='views', lookup_expr='gt')
    views__lt = NumberFilter(field_name='views', lookup_expr='lt')
    category = AllValuesMultipleFilter()
    hidden = AllValuesFilter(field_name='shadowhidden', empty_label='Hidden')
    username = CharFilter(field_name='user__username', label='Username')
    user = CharFilter()

    class Meta:
        model = Sponsortime
        fields = ['votes__gt', 'votes__lt', 'views__gt', 'views__lt', 'category', 'hidden', 'uuid']


class UsernameFilter(FilterSet):
    votes__gt = NumberFilter(field_name='votes', lookup_expr='gt')
    votes__lt = NumberFilter(field_name='votes', lookup_expr='lt')
    views__gt = NumberFilter(field_name='views', lookup_expr='gt')
    views__lt = NumberFilter(field_name='views', lookup_expr='lt')
    category = AllValuesMultipleFilter()
    hidden = AllValuesFilter(field_name='shadowhidden', empty_label='Hidden')
    user = CharFilter()

    class Meta:
        model = Sponsortime
        fields = ['videoid', 'votes__gt', 'votes__lt', 'views__gt', 'views__lt', 'category', 'hidden', 'uuid']


class UserIDFilter(FilterSet):
    votes__gt = NumberFilter(field_name='votes', lookup_expr='gt')
    votes__lt = NumberFilter(field_name='votes', lookup_expr='lt')
    views__gt = NumberFilter(field_name='views', lookup_expr='gt')
    views__lt = NumberFilter(field_name='views', lookup_expr='lt')
    category = AllValuesMultipleFilter()
    hidden = AllValuesFilter(field_name='shadowhidden', empty_label='Hidden')

    class Meta:
        model = Sponsortime
        fields = ['videoid', 'votes__gt', 'votes__lt', 'views__gt', 'views__lt', 'category', 'hidden', 'uuid']
