from oscar.core.loading import get_model
from apps.partner_api.tasks import upload_image

ProductImage = get_model('catalogue', 'ProductImage')

PRODUCT = 'product'


def upload_image_product(sender, instance, created, **kwargs):
    if instance.original:
        upload_image.delay(PRODUCT, instance.id)
