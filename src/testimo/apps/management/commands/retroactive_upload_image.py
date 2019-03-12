from django.core.management import BaseCommand
from oscar.core.loading import get_model

from apps.partner_api.tasks import upload_image

ProductImage = get_model('catalogue', 'ProductImage')
Banner = get_model('campaign', 'Banner')
BannerMini = get_model('campaign', 'BannerMini')
Endorsement = get_model('campaign', 'Endorsement')


class Command(BaseCommand):
    help = "Retroactive Image Upload"

    def handle(self, *args, **options):
        # upload product image
        products = ProductImage.objects.filter(original__isnull=False).exclude(original="")
        for p in products:
            upload_image.delay('product', p.id)

        # upload banner image
        banner_mobile = Banner.objects.filter(image_mobile__isnull=False).exclude(image_mobile="")
        for bm in banner_mobile:
            upload_image.delay('banner', bm.id, 'mobile')

        banner_desktop = Banner.objects.filter(image_desktop__isnull=False).exclude(image_desktop="")
        for bm in banner_desktop:
            upload_image.delay('banner', bm.id, 'desktop')

        # upload mini banner
        banner_mini = BannerMini.objects.filter(image__isnull=False).exclude(image="")
        for bmn in banner_mini:
            upload_image.delay('bannermini', bmn.id)

        # upload mini banner
        endorsement = Endorsement.objects.filter(image__isnull=False).exclude(image="")
        print(endorsement)
        for end in endorsement:
            upload_image.delay('endorsement', end.id)






