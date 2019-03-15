from itertools import chain

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.db.models.signals import post_save

from django.utils.translation import ugettext_lazy as _
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductImage
from django.core.exceptions import ValidationError
from apps.templatetags.api_tags import get_oss_presigned_url

from meta.models import ModelMeta
from sorl.thumbnail import get_thumbnail
from oscar.core.loading import get_class, get_model

AllProductManager = get_class('catalogue.managers', 'AllProductManager')
Benefit = get_model('offer', 'Benefit')
Range = get_model('offer', 'Range')
ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Product(ModelMeta, AbstractProduct):

    highlight = models.BooleanField(_("Highlight Product"),
                                    default=False)

    all = AllProductManager()

    _metadata = {
        'title': 'title',
        'description': 'get_description',
        'url': 'get_absolute_url',
        'image': 'get_meta_image',
        'og_type': 'product',
        'og_description': 'get_description',
        'gplus_type': 'product',
        'gplus_description': 'get_description',
        'twitter_type': 'product',
        'twitter_description': 'get_description',
        'site_name': settings.OSCAR_SHOP_NAME,
        'published_time': 'date_created',
        'modified_time': 'get_date',
        'locale': 'ID',
        'extra_props': 'get_extra_props',
    }

    def get_description(self):
        return strip_tags(self.description)

    def get_meta_image(self):
        return self.primary_image().get_image

    def get_date(self, param):
        if param == 'published_time' or param == 'modified_time':
            return self.date_updated.strftime('%Y-%m-%dT%H:%M:%S:%z')
        return self.date_created

    def get_absolute_url(self):
        return reverse('catalogue:detail', kwargs={'product_slug': self.slug, 'pk': self.id})

    def get_extra_props(self):
        return {
            'product:category': self.product_class,
        }

    def _clean_child(self):
        """
        Validates a child product
        """
        if not self.parent_id:
            raise ValidationError(_("A child product needs a parent."))
        if self.parent_id and not self.parent.is_parent:
            raise ValidationError(
                _("You can only assign child products to parent products."))
        if self.product_class:
            raise ValidationError(
                _("A child product can't have a product class."))
        if self.pk and self.categories.exists():
            pass
        # Note that we only forbid options on product level
        if self.pk and self.product_options.exists():
            raise ValidationError(
                _("A child product can't have options."))

    # =======
    # Helpers
    # =======

    def get_range_product_by_product(self):
        ranges = Range.objects.filter(rangeproduct__product_id=self)
        return ranges

    def _get_product_categories_ancestors_and_self(self):
        flatten_categories = []
        for category in self.categories.all():
            ancestors = category.get_ancestors_and_self()
            for a in ancestors:
                flatten_categories.append(a)
        return flatten_categories

    def get_range_category_by_product(self):
        ranges = Range.objects.filter(included_categories__in=self._get_product_categories_ancestors_and_self())\
                              .exclude(excluded_products=self)
        return ranges

    def get_offer_discounts(self):
        range_product = self.get_range_product_by_product()
        range_category = self.get_range_category_by_product()
        ranges = list(chain(range_product, range_category))
        offer_discounts = ConditionalOffer.active.filter(
            condition__range__in=ranges, offer_type=ConditionalOffer.SITE).order_by('-priority').first()
        return offer_discounts

    def is_available_offer(self, offer):

        available_product_discount = [Benefit.FIXED, Benefit.PERCENTAGE, Benefit.FIXED_PRICE]
        is_available = False
        if offer:
            is_available = True if offer.benefit.type in available_product_discount else False
        return is_available

    def get_tag_data(self, price, variant, **kwargs):
        uri_method = kwargs.get('url', None)
        position = kwargs.get('position', None)
        image_missing = isinstance(self.primary_image(), dict)
        product = {
            'name': self.get_title(),
            'product_id': self.id,
            'price': int(price) if price else None,
            'category': [c.name for c in self.get_categories().all()],
            'variant': variant,
            'image_url': uri_method(self.primary_image().get_image) if not image_missing else None,
            'quantity': kwargs.get('quantity', None),
            'url': uri_method() if uri_method else None,
            'sku': kwargs.get('sku', None)
        }
        if position:
            product['position'] = position
        return product

    def primary_image(self):
        """
        Returns the primary image for a product. Usually used when one can
        only display one product image, e.g. in a list of products.
        """
        images = self.get_all_images()
        ordering = self.images.model.Meta.ordering
        if not ordering or ordering[0] != 'display_order':
            # Only apply order_by() if a custom model doesn't use default
            # ordering. Applying order_by() busts the prefetch cache of
            # the ProductManager
            images = images.order_by('display_order')
        try:
            return images[0]
        except IndexError:
            # We return a dict with fields that mirror the key properties of
            # the ProductImage class so this missing image can be used
            # interchangeably in templates.  Strategy pattern ftw!
            return {
                'original': self.get_missing_image(),
                'caption': '',
                'is_missing': True,
                'get_image': settings.IMAGE_NOT_FOUND_PATH
            }

    # ==========
    # Properties
    # ==========

    @property
    def offer_discounts(self):
        context = dict()
        offer = self.get_offer_discounts()
        context['is_available'] = self.is_available_offer(offer)
        context['discount'] = offer
        return context


class ProductImage(AbstractProductImage):
    original = models.ImageField(
        _("Original"), upload_to=settings.OSCAR_IMAGE_FOLDER, max_length=255, blank=True, null=True)
    oss_image = models.CharField(max_length=200, blank=True, null=True)

    @property
    def get_image(self):
        image_size = settings.PRODUCT_IMAGE
        height = image_size['height']
        width = image_size['width']
        if self.original:
            try:
                image = get_thumbnail(self.original, f'{height}x{width}')
                return image.url
            except:
                return settings.IMAGE_NOT_FOUND_PATH
        if self.oss_image:
            return get_oss_presigned_url(self.oss_image, image_size)
        return ''


from oscar.apps.catalogue.models import *

from .signals import upload_image_product

post_save.connect(upload_image_product, sender=ProductImage, dispatch_uid='ProductImage.upload_image_product')
