from django.core.management import BaseCommand
from oscar.core.loading import get_model

from apps.partner_api.tasks import upload_image

ProductImage = get_model('catalogue', 'ProductImage')
Banner = get_model('campaign', 'Banner')
BannerMini = get_model('campaign', 'BannerMini')
Endorsement = get_model('campaign', 'Endorsement')

PRODUCT = 'product'
BANNER = 'banner'
BANNERMINI = 'bannermini'
ENDORSEMENT = 'endorsement'
MOBILE = 'mobile'
DESKTOP = 'desktop'


class Command(BaseCommand):
    help = "Retroactive Image Upload"

    def handle(self, *args, **options):
        # upload product image
        products = ProductImage.objects.filter(original__isnull=False).exclude(original="")
        for p in products:
            upload_image.delay(PRODUCT, p.id)

        # upload banner image
        banner_mobile = Banner.objects.filter(image_mobile__isnull=False).exclude(image_mobile="")
        for bm in banner_mobile:
            upload_image.delay(BANNER, bm.id, MOBILE)

        banner_desktop = Banner.objects.filter(image_desktop__isnull=False).exclude(image_desktop="")
        for bm in banner_desktop:
            upload_image.delay(BANNER, bm.id, DESKTOP)

        # upload mini banner
        banner_mini = BannerMini.objects.filter(image__isnull=False).exclude(image="")
        for bmn in banner_mini:
            upload_image.delay(BANNERMINI, bmn.id)

        # upload mini banner
        endorsement = Endorsement.objects.filter(image__isnull=False).exclude(image="")
        for end in endorsement:
            upload_image.delay(ENDORSEMENT, end.id)






