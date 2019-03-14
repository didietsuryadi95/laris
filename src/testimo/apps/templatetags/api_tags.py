import logging
import oss2

from django import template
from django.conf import settings

register = template.Library()

logger = logging.getLogger('testimo')


@register.simple_tag()
def get_oss_presigned_url(remote_filepath, resize=None, bucket_name=settings.OSS_BUCKET_NAME, expires_in_seconds=3600):
    endpoint = settings.OSS_ENDPOINT
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    extra_params = {}
    extra_headers = {'Cache-Control': 'max-age=31536000'}
    if resize:
        extra_params = {"x-oss-process": f"image/resize,m_fill,h_{resize['height']},w_{resize['width']}"
                        f"/quality,q_{settings.IMAGE_QUALITY}/format,{settings.IMAGE_FORMAT}"}
    url = bucket.sign_url('GET', remote_filepath, expires_in_seconds, headers=extra_headers, params=extra_params)
    logger.info({
        'bucket_name': bucket_name,
        'remote_filepath': remote_filepath,
        'url': url
    })
    return url.split('&OSSAccessKeyId')[0]
