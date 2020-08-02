from django.utils.html import format_html

import django_tables2 as tables


class UsernameColumn(tables.Column):
    def render(self, value):
        return format_html(f'<textarea class="form-control" name="Username" readonly>{value}</textarea>'
                           f'<button onclick="copyToClipboard(\'{value}\');">✂</button>'
                           f'<a href="/username/{value}/">🔗</a>')
