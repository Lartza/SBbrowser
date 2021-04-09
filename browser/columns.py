# SPDX-License-Identifier: AGPL-3.0-or-later
import datetime
import django_tables2 as tables

from django.db.models import F, QuerySet


class LengthColumn(tables.Column):
    def render(self, value: float) -> datetime.timedelta:
        return datetime.timedelta(seconds=value)

    def order(self, queryset: QuerySet, is_descending: bool) -> (QuerySet, bool):
        queryset = queryset.annotate(
            length=F("endtime") - F("starttime")
        ).order_by(("-" if is_descending else "") + "length")
        return queryset, True
