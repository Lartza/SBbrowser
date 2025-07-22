# SPDX-License-Identifier: AGPL-3.0-or-later
import datetime

import django_tables2 as tables
from django.db.models import F, QuerySet
from django.utils.html import format_html


class LengthColumn(tables.Column):
    def render(self, value: float) -> str:
        time = str(datetime.timedelta(seconds=value))
        try:
            time, decimal = time.split(".")
            decimal = decimal.rstrip("0")
            if len(decimal) > 3:
                return format_html("{}.<strong>{}</strong>", time, decimal)
            return f"{time}.{decimal}"
        except ValueError:
            return time

    def order(self, queryset: QuerySet, is_descending: bool) -> tuple[QuerySet, bool]:
        queryset = queryset.annotate(length=F("endtime") - F("starttime")).order_by(
            ("-" if is_descending else "") + "length"
        )
        return queryset, True
