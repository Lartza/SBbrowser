# SPDX-License-Identifier: AGPL-3.0-or-later
from .models import Sponsortime
from .columns import *


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
    username = tables.TemplateColumn('<textarea class="form-control" name="Username" readonly>{{ value }}</textarea>'
                                     '<button onclick="copyToClipboard(\'{{ value }}\');">✂</button>'
                                     '<a href="/username/{{ value }}/">🔗</a>', accessor='user__username')
    length = LengthColumn()

    class Meta:
        model = Sponsortime
        exclude = ('incorrectvotes', 'user')
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category',
                    'shadowhidden', 'uuid', 'username')

    @staticmethod
    def render_timesubmitted(value: float) -> str:
        return datetime.datetime.utcfromtimestamp(value/1000.).strftime('%Y-%m-%d %H:%M:%S')

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
    def render_votes(value: int) -> str:
        if value <= -2:
            return f'{value} ❌'
        return str(value)

    @staticmethod
    def render_shadowhidden(value: int) -> str:
        if value == 1:
            return '❌'
        return '—'

    @staticmethod
    def order_username(qs: QuerySet, is_descending: bool) -> (QuerySet, bool):
        if is_descending:
            qs = qs.select_related('user').order_by(F('user__username').desc(nulls_last=True))
        else:
            qs = qs.select_related('user').order_by(F('user__username').asc(nulls_last=True))
        return qs, True


class VideoTable(SponsortimeTable):
    class Meta:
        exclude = ('videoid',)
        sequence = ('timesubmitted', 'starttime', 'endtime', 'length', 'votes', 'views', 'category', 'shadowhidden',
                    'uuid', 'username')


class UsernameTable(SponsortimeTable):
    class Meta:
        exclude = ('username',)
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category',
                    'shadowhidden', 'uuid')


class UserIDTable(SponsortimeTable):
    class Meta:
        exclude = ('username', 'userid')
        sequence = ('timesubmitted', 'videoid', 'starttime', 'endtime', 'length', 'votes', 'views', 'category',
                    'shadowhidden')
