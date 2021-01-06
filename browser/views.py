# SPDX-License-Identifier: AGPL-3.0-or-later
from dateutil.parser import isoparse
import timeago
from typing import Dict, Any

from django.db.models import Sum
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Config, Username, Nosegment
from .tables import *
from .filters import *


def updated() -> str:
    date = isoparse(Config.objects.get(key='updated').value)
    now = datetime.datetime.now()
    return f'{date.strftime("%Y-%m-%d %H:%M:%S")} ({timeago.format(date, now)})'


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
        nosegments = list(Nosegment.objects.filter(videoid=self.videoid).only('category').values_list('category', flat=True))
        if nosegments:
            context['nosegments'] = ', '.join(nosegments)
        else:
            context['nosegments'] = '—'
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
        context['uniques'] = Username.objects.filter(username=self.username)
        context['uniques_count'] = context['uniques'].count()
        context['submissions'] = Sponsortime.objects.filter(user__username=self.username).count()
        context['ignored'] = Sponsortime.objects.filter(user__username=self.username).filter(votes__lte=-2).count()
        context['percent_ignored'] = round(context['ignored'] / context['submissions'] * 100, 1)
        context['views'] = Sponsortime.objects.filter(user__username=self.username).aggregate(Sum('views'))['views__sum']
        context['ignored_views'] = Sponsortime.objects.filter(user__username=self.username).filter(votes__lte=-2).aggregate(Sum('views'))['views__sum']
        context['percent_ignored_views'] = round(context['ignored_views'] / context['views'] * 100, 1)
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
        context['percent_ignored'] = round(context['ignored'] / context['submissions'] * 100, 1)
        context['views'] = Sponsortime.objects.filter(user=self.userid).aggregate(Sum('views'))['views__sum']
        context['ignored_views'] = Sponsortime.objects.filter(user=self.userid).filter(votes__lte=-2).aggregate(Sum('views'))['views__sum']
        if context['ignored_views'] is None:
            context['ignored_views'] = 0
            context['percent_ignored_views'] = 0.0
        else:
            context['percent_ignored_views'] = round(context['ignored_views'] / context['views'] * 100, 1)
        context['updated'] = updated()
        return context

    table_class = UserIDTable
    model = Sponsortime
    template_name = 'browser/userid.html'
    filterset_class = UserIDFilter
