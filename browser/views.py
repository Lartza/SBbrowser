from dateutil.parser import isoparse

from django_filters import FilterSet, CharFilter, NumberFilter, AllValuesFilter, AllValuesMultipleFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Sponsortime, Config
from .tables import SponsortimeTable, VideoTable, UsernameTable, UserIDTable


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


class FilteredSponsortimeListView(SingleTableMixin, FilterView):
    queryset = Sponsortime.objects.order_by('-timesubmitted')
    table_class = SponsortimeTable
    model = Sponsortime
    template_name = 'browser/index.html'
    filterset_class = SponsortimeFilter

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FilteredSponsortimeListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['updated'] = isoparse(Config.objects.get(key='updated').value).strftime('%Y-%m-%d %H:%M:%S')
        return context


class FilteredVideoListView(SingleTableMixin, FilterView):
    def get_queryset(self):
        self.videoid = self.kwargs['videoid']
        return Sponsortime.objects.filter(videoid=self.videoid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FilteredVideoListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['videoid'] = self.videoid
        context['updated'] = isoparse(Config.objects.get(key='updated').value).strftime('%Y-%m-%d %H:%M:%S')
        return context

    table_class = VideoTable
    model = Sponsortime
    template_name = 'browser/video.html'
    filterset_class = VideoFilter


class FilteredUsernameListView(SingleTableMixin, FilterView):
    def get_queryset(self):
        self.username = self.kwargs['username']
        return Sponsortime.objects.filter(user__username=self.username).order_by('-timesubmitted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FilteredUsernameListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['username'] = self.username
        context['updated'] = isoparse(Config.objects.get(key='updated').value).strftime('%Y-%m-%d %H:%M:%S')
        return context

    table_class = UsernameTable
    model = Sponsortime
    template_name = 'browser/username.html'
    filterset_class = UsernameFilter


class FilteredUserIDListView(SingleTableMixin, FilterView):
    def get_queryset(self):
        self.userid = self.kwargs['userid']
        return Sponsortime.objects.filter(user=self.userid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FilteredUserIDListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context['userid'] = self.userid
        context['updated'] = isoparse(Config.objects.get(key='updated').value).strftime('%Y-%m-%d %H:%M:%S')
        return context

    table_class = UserIDTable
    model = Sponsortime
    template_name = 'browser/userid.html'
    filterset_class = UserIDFilter
