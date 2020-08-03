import datetime

from django.db.models import F

import django_tables2 as tables
from .models import Sponsortime
from .columns import UsernameColumn


class SponsortimeTable(tables.Table):
    videoid = tables.TemplateColumn('<a href="/video/{{ value }}/">{{ value }}</a>'
                                    '<button onclick="copyToClipboard(\'{{ value }}\');">✂</button>'
                                    '<a href="https://youtu.be/{{ value }}">YT</a>')
    uuid = tables.TemplateColumn('<textarea class="form-control" name="UUID" readonly>{{ value }}</textarea>'
                                 '<button onclick="copyToClipboard(\'{{ value }}\');">✂</button>')
    userid = tables.TemplateColumn('<textarea class="form-control" name="UserID" readonly>{{ value }}</textarea>'
                                   '<button onclick="copyToClipboard(\'{{ value }}\');">✂</button>'
                                   '<a href="/userid/{{ value }}/">🔗</a>',
                                   verbose_name='UserID', accessor='user_id')
    username = UsernameColumn(accessor='user__username')
    length = tables.Column()

    class Meta:
        model = Sponsortime
        exclude = ('incorrectvotes', 'user')
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category', 'shadowhidden',
                    'uuid', 'username')

    @staticmethod
    def render_timesubmitted(value):
        return datetime.datetime.utcfromtimestamp(value/1000.).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def render_starttime(value):
        if value < 0:
            return '-' + str(datetime.timedelta(seconds=-value))
        return datetime.timedelta(seconds=value)

    @staticmethod
    def render_endtime(value):
        if value < 0:
            return '-' + str(datetime.timedelta(seconds=-value))
        return datetime.timedelta(seconds=value)

    @staticmethod
    def render_votes(value):
        if value <= -2:
            return f'{value} ❌'
        return value

    @staticmethod
    def render_shadowhidden(value):
        if value == 1:
            return '❌'
        return '—'

    @staticmethod
    def order_username(qs, is_descending):
        if is_descending:
            qs = qs.select_related('user').order_by(F('user__username').desc(nulls_last=True))
        else:
            qs = qs.select_related('user').order_by(F('user__username').asc(nulls_last=True))
        return qs, True

    @staticmethod
    def render_length(value):
        return datetime.timedelta(seconds=value)

    @staticmethod
    def order_length(qs, is_descending):
        qs = qs.annotate(
            length=F("endtime") - F("starttime")
        ).order_by(("-" if is_descending else "") + "length")
        return qs, True


class VideoTable(SponsortimeTable):
    class Meta:
        exclude = ('videoid',)
        sequence = ('timesubmitted', 'starttime', 'endtime', 'length', 'votes', 'views', 'category', 'shadowhidden', 'uuid',
                    'username')


class UsernameTable(SponsortimeTable):
    class Meta:
        exclude = ('username',)
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category', 'shadowhidden',
                    'uuid')


class UserIDTable(SponsortimeTable):
    class Meta:
        exclude = ('username', 'userid')
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category', 'shadowhidden')
