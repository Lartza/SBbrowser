# SPDX-License-Identifier: AGPL-3.0-or-later
import datetime

from django.utils.html import format_html
from django.db.models import F, QuerySet

import django_tables2 as tables

from .models import Sponsortime, Vipuser
from .columns import LengthColumn


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
    username = tables.TemplateColumn('{% if value %}'
                                     '<textarea class="form-control" name="Username" readonly>{{ value }}</textarea>'
                                     '<button onclick="copyToClipboard(\'{{ value }}\');">✂</button>'
                                     '<a href="/username/{{ value }}/">🔗</a>'
                                     '{% else %}—{% endif %}', accessor='user__username')
    length = LengthColumn()

    class Meta: # noqa
        model = Sponsortime
        exclude = ('incorrectvotes', 'user', 'videoduration', 'locked', 'service', 'hidden', 'hashedvideoid')
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category',
                    'shadowhidden', 'uuid', 'username')

    @staticmethod
    def render_timesubmitted(value: float) -> str:
        return datetime.datetime.utcfromtimestamp(value / 1000.).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def render_starttime(value: float) -> str:
        if value < 0:
            return '-' + str(datetime.timedelta(seconds=-value))
        return str(datetime.timedelta(seconds=value))

    @staticmethod
    def render_endtime(value: float) -> str:
        if value < 0:
            return '-' + str(datetime.timedelta(seconds=-value))
        return str(datetime.timedelta(seconds=value))

    @staticmethod
    def render_votes(value: int, record) -> str:
        hidden = ''
        if value <= -2:
            hidden = '<span title="This segment is not sent to users">❌</span>'
        if Vipuser.objects.filter(userid=record.user_id).exists():
            return format_html(f'{value}{hidden} <span title="This user is a VIP">👑</span>')
        return format_html(f"{value}{hidden}")

    @staticmethod
    def render_shadowhidden(value: int) -> str:
        if value == 1:
            return format_html('<span title="This segment is not sent to users">❌</span>')
        return '—'

    @staticmethod
    def order_username(queryset: QuerySet, is_descending: bool) -> (QuerySet, bool):
        if is_descending:
            queryset = queryset.select_related('user').order_by(F('user__username').desc(nulls_last=True))
        else:
            queryset = queryset.select_related('user').order_by(F('user__username').asc(nulls_last=True))
        return queryset, True


class VideoTable(SponsortimeTable):
    class Meta: # noqa
        exclude = ('videoid',)
        sequence = ('timesubmitted', 'starttime', 'endtime', 'length', 'votes', 'views', 'category', 'shadowhidden',
                    'uuid', 'username')


class UsernameTable(SponsortimeTable):
    class Meta: # noqa
        exclude = ('username',)
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category',
                    'shadowhidden', 'uuid')


class UserIDTable(SponsortimeTable):
    class Meta: # noqa
        exclude = ('username', 'userid')
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category',
                    'shadowhidden')
