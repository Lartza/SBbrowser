# SPDX-License-Identifier: AGPL-3.0-or-later
import datetime
from typing import Dict, Any
from urllib.parse import urlparse, parse_qs
from math import ceil, floor

from dateutil.parser import isoparse
import timeago

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Sum, QuerySet, Q
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView

from .models import Config, Username, Lockcategory, Sponsortime, Vipuser, Warnings
from .tables import SponsortimeTable, VideoTable, UsernameTable, UserIDTable
from .filters import VideoFilter, UsernameFilter, UserIDFilter


def updated() -> str:
    date = isoparse(Config.objects.get(key='updated').value)
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return f'{date.strftime("%Y-%m-%d %H:%M:%S")} ({timeago.format(date, now)})'


def get_yt_video_id(url):
    """Returns Video_ID extracting from the given url of Youtube"""

    if url.startswith(('youtu', 'www')):
        url = 'http://' + url

    query = urlparse(url)

    if query.hostname is None:
        raise ValueError('No hostname found')

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    raise ValueError('Not a YouTube URL')


def populate_context(context, filter_args):
    context['user_submissions'] = Sponsortime.objects.filter(**filter_args).count()
    context['user_ignored'] = Sponsortime.objects.filter(**filter_args).filter(votes__lte=-2).count()
    context['user_hidden'] = Sponsortime.objects.filter(**filter_args).filter(votes__gte=-1).filter(
        Q(hidden=1) | Q(shadowhidden=1)).count()
    if context['user_submissions'] != 0:
        context['percent_ignored'] = round(context['user_ignored'] / context['user_submissions'] * 100, 1)
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


def populate_context_video_details(context, videoid):
    context['videoid'] = videoid
    context['submissions'] = Sponsortime.objects.filter(videoid=videoid).count()
    context['ignored'] = Sponsortime.objects.filter(videoid=videoid).filter(votes__lte=-2).count()
    context['hidden'] = Sponsortime.objects.filter(videoid=videoid).filter(votes__gte=-1).filter(
        Q(hidden=1) | Q(shadowhidden=1)).count()

    context['lockcategories_skip'] = context['lockcategories_mute'] = context['lockcategories_full'] = '—'
    lockcategories = Lockcategory.objects.filter(videoid=videoid)
    lockcategories_skip = list(lockcategories.filter(actiontype='skip').only('category')
                               .values_list('category', flat=True))
    lockcategories_mute = list(lockcategories.filter(actiontype='mute').only('category')
                               .values_list('category', flat=True))
    lockcategories_full = list(lockcategories.filter(actiontype='full').only('category')
                               .values_list('category', flat=True))
    if lockcategories_skip:
        context['lockcategories_skip'] = ', '.join(lockcategories_skip)
    if lockcategories_mute:
        context['lockcategories_mute'] = ', '.join(lockcategories_mute)
    if lockcategories_full:
        context['lockcategories_full'] = ', '.join(lockcategories_full)


class FilteredSponsortimeListView(SingleTableView):
    table_class = SponsortimeTable
    template_name = 'browser/index.html'

    def get_queryset(self) -> list:
        qs = Sponsortime.objects.order_by('-timesubmitted')[:10]
        return list(qs)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['updated'] = updated()
        return context

    def get(self, request, *args, **kwargs):
        videoid = request.GET.get('videoid')
        if videoid:
            return HttpResponseRedirect(reverse('video', args=[videoid]))
        username = request.GET.get('username')
        if username:
            return HttpResponseRedirect(reverse('username', args=[username]))
        userid = request.GET.get('userid')
        if userid:
            return HttpResponseRedirect(reverse('userid', args=[userid]))
        uuid = request.GET.get('uuid')
        if uuid:
            return HttpResponseRedirect(reverse('uuid', args=[uuid]))
        return super().get(request, *args, **kwargs)


class FilteredVideoListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.videoid = None

    def get_queryset(self) -> QuerySet:
        self.videoid = self.kwargs['videoid']
        return Sponsortime.objects.filter(videoid=self.videoid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)

        populate_context_video_details(context, self.videoid)
        context['updated'] = updated()
        return context

    table_class = VideoTable
    template_name = 'browser/video.html'
    filterset_class = VideoFilter


class FilteredUsernameListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.username = None

    def get_queryset(self) -> QuerySet:
        self.username = self.kwargs['username']
        query = Sponsortime.objects.filter(user__username=self.username).order_by('-timesubmitted')
        if not query.exists():
            raise Http404
        return query

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        filter_args = {'user__username': self.username}

        context['username'] = self.username
        context['uniques'] = Username.objects.filter(username=self.username)
        context['uniques_count'] = context['uniques'].count()

        populate_context(context, filter_args)

        return context

    table_class = UsernameTable
    template_name = 'browser/username.html'
    filterset_class = UsernameFilter


class FilteredUserIDListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.userid = None

    def get_queryset(self) -> QuerySet:
        self.userid = self.kwargs['userid']
        query = Sponsortime.objects.filter(user=self.userid).order_by('-timesubmitted')
        if not query.exists():
            raise Http404
        return query

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        filter_args = {'user': self.userid}

        context['userid'] = self.userid
        try:
            context['username'] = Username.objects.get(userid=self.userid).username
        except Username.DoesNotExist:
            context['username'] = '—'
        context['vip'] = Vipuser.objects.filter(userid=self.userid).exists()
        context['warnings'] = Warnings.objects.filter(userid=self.userid, enabled=1).values_list('reason', flat=True)

        populate_context(context, filter_args)

        return context

    table_class = UserIDTable
    template_name = 'browser/userid.html'
    filterset_class = UserIDFilter


class FilteredUUIDListView(SingleTableMixin, FilterView):
    def __init__(self):
        super().__init__()
        self.videoid = None
        self.uuid = None

    def get_queryset(self) -> QuerySet:
        try:
            self.uuid = Sponsortime.objects.get(uuid=self.kwargs['uuid'])
        except Sponsortime.DoesNotExist:
            raise Http404
        self.videoid = self.uuid.videoid
        return Sponsortime.objects.filter(videoid=self.videoid).order_by('-timesubmitted')

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)

        filter_args = {'user': self.uuid.user_id}
        try:
            context['username'] = self.uuid.user.username
        except Username.DoesNotExist:
            context['username'] = '—'
        context['vip'] = Vipuser.objects.filter(userid=self.uuid.user_id).exists()

        context['uuid'] = self.uuid
        context['submitted'] = SponsortimeTable.render_timesubmitted(self.uuid.timesubmitted)
        context['starttime'] = SponsortimeTable.render_starttime(self.uuid.starttime)
        context['endtime'] = SponsortimeTable.render_endtime(self.uuid.endtime)
        context['length'] = datetime.timedelta(seconds=self.uuid.length())
        context['actiontype'] = SponsortimeTable.render_actiontype(self.uuid.actiontype)
        context['duration'] = datetime.timedelta(seconds=self.uuid.videoduration)
        context['uuid_hidden'] = SponsortimeTable.render_hidden(self.uuid.hidden)
        context['shadowhidden'] = SponsortimeTable.render_shadowhidden(self.uuid.shadowhidden)

        class FakeRecord:
            def __init__(self, locked, user_id):
                self.locked = locked
                self.user_id = user_id

        context['votes'] = SponsortimeTable.render_votes(self.uuid.votes, FakeRecord(self.uuid.locked,
                                                                                     self.uuid.user_id))
        context['start'] = max(floor(self.uuid.starttime) - 2, 0)
        context['end'] = ceil(self.uuid.endtime) + 4

        populate_context_video_details(context, self.videoid)
        populate_context(context, filter_args)

        return context

    table_class = VideoTable
    template_name = 'browser/uuid.html'
    filterset_class = VideoFilter
