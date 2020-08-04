import datetime
import django_tables2 as tables

from django.utils.html import format_html
from django.db.models import F


class UsernameColumn(tables.Column):
    def render(self, value):
        return format_html(f'<textarea class="form-control" name="Username" readonly>{value}</textarea>'
                           f'<button onclick="copyToClipboard(\'{value}\');">✂</button>'
                           f'<a href="/username/{value}/">🔗</a>')


class LengthColumn(tables.Column):
    def render(self, value):
        return datetime.timedelta(seconds=value)

    def order(self, qs, is_descending):
        qs = qs.annotate(
            length=F("endtime") - F("starttime")
        ).order_by(("-" if is_descending else "") + "length")
        return qs, True
