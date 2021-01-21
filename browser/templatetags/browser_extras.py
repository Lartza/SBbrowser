from django import template

from browser.models import Vipuser

register = template.Library()


@register.simple_tag
def is_vip(userid) -> bool:
    return Vipuser.objects.filter(userid=userid).exists()
