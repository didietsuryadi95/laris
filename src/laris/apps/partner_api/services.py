import logging
import oss2

from django.conf import settings

from oscar.core.loading import get_model

ProductImage = get_model('catalogue', 'ProductImage')
Banner = get_model('campaign', 'Banner')
BannerMini = get_model('campaign', 'BannerMIni')
Endorsement = get_model('campaign', 'Endorsement')

logger = logging.getLogger('laris')

PRODUCT = 'product'
BANNER = 'banner'
BANNERMINI = 'bannermini'
ENDORSEMENT = 'endorsement'
MOBILE = 'mobile'
DESKTOP = 'desktop'


def construct_remote_filepath(image_type, image_id, options=None):
    """Using some input constructing folder structure in cloud storage"""
    local_path = None
    remote_path = None
    if image_type == PRODUCT:
        img = ProductImage.objects.get(pk=image_id)
        local_path = img.original.path
        remote_path = img.original.name
    elif image_type == BANNER:
        img = Banner.objects.get(pk=image_id)
        if options == DESKTOP:
            local_path = img.image_desktop.path
            remote_path = img.image_desktop.name
        elif options == MOBILE:
            local_path = img.image_mobile.path
            remote_path = img.image_mobile.name
    elif image_type == BANNERMINI:
        img = BannerMini.objects.get(pk=image_id)
        local_path = img.image.path
        remote_path = img.image.name
    elif image_type == ENDORSEMENT:
        img = Endorsement.objects.get(pk=image_id)
        local_path = img.image.path
        remote_path = img.image.name
    # construct destination name

    full_remote_path = f"uploads/{remote_path}"
    return local_path, full_remote_path


def update_image_upload_status(image_type, image_id, remote_url, options=None):
    if image_type == PRODUCT:
        img = ProductImage.objects.get(pk=image_id)
        img.original.delete()
        img.oss_image = remote_url
        img.save()
    elif image_type == BANNER:
        img = Banner.objects.get(pk=image_id)
        if options == DESKTOP:
            img.image_desktop.delete()
            img.oss_image_desktop = remote_url
            img.save()
        elif options == MOBILE:
            img.image_mobile.delete()
            img.oss_image_mobile = remote_url
            img.save()
    elif image_type == BANNERMINI:
        img = BannerMini.objects.get(pk=image_id)
        img.image.delete()
        img.oss_image = remote_url
        img.save()
    elif image_type == ENDORSEMENT:
        img = Endorsement.objects.get(pk=image_id)
        img.image.delete()
        img.oss_image = remote_url
        img.save()


def upload_file_to_oss(local_filepath, remote_filepath, bucket_name=settings.OSS_BUCKET_NAME):
    endpoint = settings.OSS_ENDPOINT
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    logger.info({
        'action': 'uploading_file',
        'bucket_name': bucket_name,
        'local_filepath': local_filepath,
        'remote_filepath': remote_filepath,
    })
    bucket.put_object_from_file(remote_filepath, local_filepath)
    logger.info({
        'status': 'uploaded',
        'bucket_name': bucket_name,
        'remote_filepath': remote_filepath,
    })
