from django.conf import settings
from django.template.loader import render_to_string
from apps.templatetags.utils_tags import get_scheme, get_full_current_site
from django.contrib.sites.shortcuts import get_current_site


def render_to_string_with_context(template_path, **kwargs):
    domain = kwargs.get('domain')
    scheme = kwargs.get('scheme')
    if not domain:
        domain = get_current_site(None).domain
    if not scheme:
        scheme = get_scheme()

    kwargs.update({
        'domain': domain,
        'scheme': scheme,
        'homepage_url': get_full_current_site(),
        'facebook': getattr(settings, 'SOCIAL_FACEBOOK', None),
        'instagram': getattr(settings, 'SOCIAL_INSTAGRAM', None),
        'twitter': getattr(settings, 'SOCIAL_TWITTER', None),
        'youtube': getattr(settings, 'SOCIAL_YOUTUBE', None)
    })
    message = render_to_string(template_path, kwargs)
    return message
