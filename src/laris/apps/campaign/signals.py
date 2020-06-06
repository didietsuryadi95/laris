from django.db.models.signals import post_save
from django.dispatch import receiver
from oscar.core.loading import get_model
from apps.partner_api.tasks import upload_image

Banner = get_model('campaign', 'Banner')
BannerMini = get_model('campaign', 'BannerMini')
Endorsement = get_model('campaign', 'Endorsement')

BANNER = 'banner'
BANNERMINI = 'bannermini'
ENDORSEMENT = 'endorsement'
MOBILE = 'mobile'
DESKTOP = 'desktop'


@receiver(post_save, sender=Banner)
def upload_image_banner(sender, instance, created, **kwargs):
    if instance.image_desktop:
        upload_image.delay(BANNER, instance.id, DESKTOP)
    if instance.image_mobile:
        upload_image.delay(BANNER, instance.id, MOBILE)


@receiver(post_save, sender=BannerMini)
def upload_image_banner_mini(sender, instance, created, **kwargs):
    if instance.image:
        upload_image.delay(BANNERMINI, instance.id)


@receiver(post_save, sender=Endorsement)
def upload_image_endorsement(sender, instance, created, **kwargs):
    if instance.image:
        upload_image.delay(ENDORSEMENT, instance.id)
