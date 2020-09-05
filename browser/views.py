from dateutil.parser import isoparse
from typing import Dict, Any

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Config, Username
from .tables import *
from .filters import *


def updated() -> str:
    return isoparse(Config.objects.get(key='updated').value).strftime('%Y-%m-%d %H:%M:%S')


class FilteredSponsortimeListView(SingleTableMixin, FilterView):
    queryset = Sponsortime.objects.order_by('-timesubmitted')
    table_class = SponsortimeTable
    model = Sponsortime
    template_name = 'browser/index.html'
    filterset_class = SponsortimeFilter

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(FilteredSponsortimeListView, self).get_context_data(**kwargs)

        context['updated'] = updated()
        return context


class FilteredVideoListView(SingleTableMixin, FilterView):
    def get_queryset(self) -> QuerySet:
        self.videoid = self.kwargs['videoid']
        return Sponsortime.objects.filter(videoid=self.videoid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:

        context = super(FilteredVideoListView, self).get_context_data(**kwargs)

        context['videoid'] = self.videoid
        context['submissions'] = Sponsortime.objects.filter(videoid=self.videoid).count()
        context['ignored'] = Sponsortime.objects.filter(videoid=self.videoid).filter(votes__lte=-2).count()
        context['updated'] = updated()
        return context

    table_class = VideoTable
    model = Sponsortime
    template_name = 'browser/video.html'
    filterset_class = VideoFilter


class FilteredUsernameListView(SingleTableMixin, FilterView):
    def get_queryset(self) -> QuerySet:
        self.username = self.kwargs['username']
        return Sponsortime.objects.filter(user__username=self.username).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(FilteredUsernameListView, self).get_context_data(**kwargs)

        context['username'] = self.username
        context['uniques'] = Username.objects.filter(username=self.username).count()
        context['submissions'] = Sponsortime.objects.filter(user__username=self.username).count()
        context['ignored'] = Sponsortime.objects.filter(user__username=self.username).filter(votes__lte=-2).count()
        context['updated'] = updated()
        return context

    table_class = UsernameTable
    model = Sponsortime
    template_name = 'browser/username.html'
    filterset_class = UsernameFilter


class FilteredUserIDListView(SingleTableMixin, FilterView):
    def get_queryset(self) -> QuerySet:
        self.userid = self.kwargs['userid']
        return Sponsortime.objects.filter(user=self.userid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super(FilteredUserIDListView, self).get_context_data(**kwargs)

        context['userid'] = self.userid
        try:
            context['username'] = Username.objects.get(userid=self.userid).username
        except Username.DoesNotExist:
            context['username'] = '—'
        context['submissions'] = Sponsortime.objects.filter(user=self.userid).count()
        context['ignored'] = Sponsortime.objects.filter(user=self.userid).filter(votes__lte=-2).count()
        context['updated'] = updated()
        return context

    table_class = UserIDTable
    model = Sponsortime
    template_name = 'browser/userid.html'
    filterset_class = UserIDFilter
