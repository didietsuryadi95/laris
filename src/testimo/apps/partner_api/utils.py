from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string


def render_to_string_with_context(template_path, **kwargs):
    domain = kwargs.get('domain')
    scheme = kwargs.get('scheme')
    if not domain:
        domain = Site.objects.last().domain
    if not scheme:
        debug = getattr(settings, 'DEBUG')
        scheme = 'https://' if not debug else 'http://'

    kwargs.update({
        'domain': domain,
        'scheme': scheme,
        'homepage_url': scheme+domain,
        'facebook': getattr(settings, 'SOCIAL_FACEBOOK', None),
        'instagram': getattr(settings, 'SOCIAL_INSTAGRAM', None),
        'twitter': getattr(settings, 'SOCIAL_TWITTER', None),
        'youtube': getattr(settings, 'SOCIAL_YOUTUBE', None)
    })
    message = render_to_string(template_path, kwargs)
    return message
