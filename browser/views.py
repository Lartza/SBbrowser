# SPDX-License-Identifier: AGPL-3.0-or-later
import datetime
from typing import Dict, Any

from dateutil.parser import isoparse
import timeago

from django.db.models import Sum, QuerySet, Q
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import Config, Username, Lockcategory, Sponsortime, Vipuser
from .tables import SponsortimeTable, VideoTable, UsernameTable, UserIDTable
from .filters import SponsortimeFilter, VideoFilter, UsernameFilter, UserIDFilter


def updated() -> str:
    date = isoparse(Config.objects.get(key='updated').value)
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return f'{date.strftime("%Y-%m-%d %H:%M:%S")} ({timeago.format(date, now)})'


def populate_context(context, filter_args) -> dict:
    context['submissions'] = Sponsortime.objects.filter(**filter_args).count()
    context['ignored'] = Sponsortime.objects.filter(**filter_args).filter(votes__lte=-2).count()
    context['hidden'] = Sponsortime.objects.filter(**filter_args).filter(votes__gte=-1).filter(
        Q(hidden=1) | Q(shadowhidden=1)).count()
    if context['submissions'] != 0:
        context['percent_ignored'] = round(context['ignored'] / context['submissions'] * 100, 1)
    else:
        context['percent_ignored'] = 0.0
    context['views'] = Sponsortime.objects.filter(**filter_args).aggregate(Sum('views'))['views__sum']
    context['ignored_views'] = Sponsortime.objects.filter(**filter_args).filter(votes__lte=-2).aggregate(Sum('views'))[
        'views__sum']
    if context['ignored_views'] is None or context['views'] == 0:
        context['ignored_views'] = 0
        context['percent_ignored_views'] = 0.0
    else:
        context['percent_ignored_views'] = round(context['ignored_views'] / context['views'] * 100, 1)
    context['updated'] = updated()
    return context


class FilteredSponsortimeListView(SingleTableMixin, FilterView):
    queryset = Sponsortime.objects.order_by('-timesubmitted')
    table_class = SponsortimeTable
    model = Sponsortime
    template_name = 'browser/index.html'
    filterset_class = SponsortimeFilter

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['updated'] = updated()
        return context


class FilteredVideoListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.videoid = None

    def get_queryset(self) -> QuerySet:
        self.videoid = self.kwargs['videoid']
        return Sponsortime.objects.filter(videoid=self.videoid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)

        context['videoid'] = self.videoid
        context['submissions'] = Sponsortime.objects.filter(videoid=self.videoid).count()
        context['ignored'] = Sponsortime.objects.filter(videoid=self.videoid).filter(votes__lte=-2).count()
        context['hidden'] = Sponsortime.objects.filter(videoid=self.videoid).filter(votes__gte=-1).filter(
            Q(hidden=1) | Q(shadowhidden=1)).count()

        context['lockcategories_skip'] = context['lockcategories_mute'] = context['lockcategories_full'] = '—'
        lockcategories = Lockcategory.objects.filter(videoid=self.videoid)
        lockcategories_skip = list(lockcategories.filter(category='skip').only('category')
                                   .values_list('category', flat=True))
        lockcategories_mute = list(lockcategories.filter(category='mute').only('category')
                                   .values_list('category', flat=True))
        lockcategories_full = list(lockcategories.filter(category='full').only('category')
                                   .values_list('category', flat=True))
        if lockcategories_skip:
            context['lockcategories_skip'] = ', '.join(lockcategories_skip)
        if lockcategories_mute:
            context['lockcategories_mute'] = ', '.join(lockcategories_mute)
        if lockcategories_full:
            context['lockcategories_full'] = ', '.join(lockcategories_full)

        context['updated'] = updated()
        return context

    table_class = VideoTable
    model = Sponsortime
    template_name = 'browser/video.html'
    filterset_class = VideoFilter


class FilteredUsernameListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.username = None

    def get_queryset(self) -> QuerySet:
        self.username = self.kwargs['username']
        return Sponsortime.objects.filter(user__username=self.username).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        filter_args = {'user__username': self.username}

        context['username'] = self.username
        context['uniques'] = Username.objects.filter(username=self.username)
        context['uniques_count'] = context['uniques'].count()

        populate_context(context, filter_args)

        return context

    table_class = UsernameTable
    model = Sponsortime
    template_name = 'browser/username.html'
    filterset_class = UsernameFilter


class FilteredUserIDListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.userid = None

    def get_queryset(self) -> QuerySet:
        self.userid = self.kwargs['userid']
        return Sponsortime.objects.filter(user=self.userid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        filter_args = {'user': self.userid}

        context['userid'] = self.userid
        try:
            context['username'] = Username.objects.get(userid=self.userid).username
        except Username.DoesNotExist:
            context['username'] = '—'
        context['vip'] = Vipuser.objects.filter(userid=self.userid).exists()

        populate_context(context, filter_args)

        return context

    table_class = UserIDTable
    model = Sponsortime
    template_name = 'browser/userid.html'
    filterset_class = UserIDFilter
