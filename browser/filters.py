# SPDX-License-Identifier: AGPL-3.0-or-later
from django_filters import CharFilter, ChoiceFilter, FilterSet, MultipleChoiceFilter, RangeFilter
from django_filters.widgets import RangeWidget

from .models import Sponsortime

FIELDS = ["videoid", "votes", "views", "category", "shadowhidden", "uuid", "username", "user"]


class CustomRangeWidget(RangeWidget):
    def __init__(self, attrs=None, from_attrs=None, to_attrs=None):
        super().__init__(attrs)

        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class UserIDFilter(FilterSet):
    votes = RangeFilter(
        widget=CustomRangeWidget(
            attrs={"type": "number", "step": 1},
            from_attrs={"placeholder": "Votes from"},
            to_attrs={"placeholder": "Votes to"},
        )
    )
    views = RangeFilter(
        widget=CustomRangeWidget(
            attrs={"type": "number", "step": 1},
            from_attrs={"placeholder": "Views from"},
            to_attrs={"placeholder": "Views to"},
        )
    )
    category = MultipleChoiceFilter(
        choices=(
            ("chapter", "Chapter"),
            ("exclusive_access", "Exclusive Access"),
            ("filler", "Filler"),
            ("poi_highlight", "Highlight"),
            ("interaction", "Interaction"),
            ("intro", "Intro"),
            ("music_offtopic", "Non-Music"),
            ("outro", "Outro"),
            ("preview", "Preview"),
            ("selfpromo", "Selfpromo"),
            ("sponsor", "Sponsor"),
        ),
        distinct=False,
    )
    category.always_filter = False
    shadowhidden = ChoiceFilter(
        choices=((0, "No"), (1, "Yes")), empty_label="Shadowhidden", method="shadowhidden_filter"
    )
    actiontype = MultipleChoiceFilter(
        choices=(
            ("chapter", "Chapter"),
            ("full", "Full Video Label"),
            ("poi", "Highlight"),
            ("mute", "Mute"),
            ("skip", "Skip"),
        ),
        distinct=False,
    )

    class Meta:
        model = Sponsortime
        fields = FIELDS
        exclude = ["username", "user"]

    @staticmethod
    def shadowhidden_filter(queryset, _name, value):
        if value == 1:
            return queryset.filter(shadowhidden__gte=1)
        return queryset.filter(shadowhidden=0)


class UsernameFilter(UserIDFilter):
    user = CharFilter()

    class Meta:
        model = Sponsortime
        fields = FIELDS
        exclude = "username"


class SponsortimeFilter(UsernameFilter):
    username = CharFilter(field_name="user__username", label="Username", lookup_expr="icontains")

    class Meta:
        model = Sponsortime
        fields = FIELDS


class VideoFilter(SponsortimeFilter):
    class Meta:
        model = Sponsortime
        fields = FIELDS
        exclude = "videoid"
