import logging
from urllib.parse import quote

from django import template
from django.conf import settings

register = template.Library()

logger = logging.getLogger('testimo')


@register.simple_tag()
def get_oss_presigned_url(remote_filepath, resize=None):
    extra_params = ""
    self_domain = settings.HOSTNAME
    if resize:
        params = f"image/resize,m_fill,h_{resize['height']},w_{resize['width']}" \
            f"/quality,q_{settings.IMAGE_QUALITY}/format,{settings.IMAGE_FORMAT}"
        extra_params = f"?x-oss-process={quote(params, safe='')}"
    url = f"{self_domain}{quote(remote_filepath, safe='')}{extra_params}"
    logger.info({
        'remote_filepath': remote_filepath,
        'url': url
    })
    return url
