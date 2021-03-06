from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def print_r(data):
    return {
        "testing": str(dir(data))
    }


def global_settings(request):
    facebook = getattr(settings, 'SOCIAL_FACEBOOK', None)
    instagram = getattr(settings, 'SOCIAL_INSTAGRAM', None)
    twitter = getattr(settings, 'SOCIAL_TWITTER', None)
    youtube = getattr(settings, 'SOCIAL_YOUTUBE', None)

    return {
        'debug': getattr(settings, 'DEBUG', None),
        'MEDIA_URL': getattr(settings, 'MEDIA_URL', None),
        # 'PAYMENT_AVAILABLE': getattr(settings, 'PAYMENT_AVAILABLE',
        # 'PAYMENT_LIST': getattr(settings, 'PAYMENT_LIST',
        'SOCIAL_FACEBOOK': facebook,
        'SOCIAL_INSTAGRAM': instagram,
        'SOCIAL_TWITTER': twitter,
        'SOCIAL_YOUTUBE': youtube,
        'SOCIAL_MEDIA': [
            {
                'link': instagram,
                'icon': 'fa fa-instagram',
                'name': '@laris_bysb'
            },
            {
                'link': facebook,
                'icon': 'fa fa-facebook',
                'name': 'Facebook'
            },
            {
                'link': twitter,
                'icon': 'fa fa-twitter',
                'name': 'Twitter'
            },
            {
                'link': youtube,
                'icon': 'fa fa-youtube-play',
                'name': 'Youtube'
            },
        ],
        'SHOP_NAME': getattr(settings, 'OSCAR_SHOP_NAME', None),
        'SCHEME': request.is_secure() and "https://" or "http://",
        'SITE_DESC': getattr(settings, 'SITE_DESCRIPTION', None),
        'IMG_LOGO': getattr(settings, 'DEFAULT_IMAGE_LOGO', ''),
        'CONTACT_NUMBER': getattr(settings, 'PARTNER_PHONE_NUMBER', ''),
        'CONTACT_WHATSAPP': getattr(settings, 'PARTNER_WHATSAPP_NUMBER', ''),
        'CONTACT_EMAIL': getattr(settings, 'PARTNER_EMAIL', ''),
        #Variable for APM frontend agent js-base
        'APM_NAME_FE': getattr(settings, 'APM_NAME_FE', None),
        'APM_URL': getattr(settings, 'APM_URL', None)

    }

