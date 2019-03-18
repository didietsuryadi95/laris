import logging
from urllib.parse import quote

from django import template
from django.conf import settings

register = template.Library()

logger = logging.getLogger('testimo')


@register.simple_tag()
def get_oss_presigned_url(remote_filepath, style=''):
    self_domain = settings.HOSTNAME
    url = f"{self_domain}{quote('thumb/'+remote_filepath, safe='')}/{style}"
    logger.info({
        'remote_filepath': remote_filepath,
        'url': url
    })
    return url
