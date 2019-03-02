from django import template
from django.conf import settings

register = template.Library()
ri = register.inclusion_tag


def gtm_tag(google_tag_id=None):
    if google_tag_id is None:
        google_tag_id = getattr(settings, 'OSCAR_GOOGLE_ANALYTICS_ID', None)
    return {
        'google_tag_id': google_tag_id
    }


ri("partials/gtm/gtm_head.html", name='gtm_head')(gtm_tag)
ri("partials/gtm/gtm_body.html", name='gtm_body')(gtm_tag)
