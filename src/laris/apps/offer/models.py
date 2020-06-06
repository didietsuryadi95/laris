from django.db.models.query import Q
from oscar.apps.offer.abstract_models import AbstractConditionalOffer as CoreAbstractConditionalOffer, \
    AbstractBenefit as CoreAbstractBenefit, AbstractCondition as CoreAbstractCondition, \
    AbstractRange as CoreAbstractRange
from django.db import models
from oscar.models import fields
from django.utils.translation import ugettext_lazy as _
from oscar.core.loading import get_model


ALLAREA = "allarea"
STATE = 'state'
DISTRICT = 'district'
SUBDISTRICT = 'subdistrict'
VILLAGE = 'village'
DESTINATION_TYPE_CHOICES = (
    ('', ''),
    (ALLAREA, 'All Area'),
    (STATE, 'State'),
    (DISTRICT, 'District'),
    (SUBDISTRICT, 'Subdistrict'),
    (VILLAGE, 'Village')
)


class ConditionalOffer(CoreAbstractConditionalOffer):
    def has_no_discounts(self, products):
        data = []
        for product in products:
            if not product.offer_discounts.get('is_available'):
                data.append(product.id)
        return data

    def products(self):
        product = get_model('catalogue', 'Product')

        cond_range = self.condition.range
        if cond_range.includes_all_products:
            queryset = product.all
        else:
            queryset = cond_range.all_products()

        exclude_products = self.has_no_discounts(queryset)
        return queryset.filter(is_discountable=True).exclude(
            Q(structure=product.PARENT) | Q(id__in=exclude_products))


class RangeDestination(models.Model):
    name = models.CharField(_("Name"), max_length=128, unique=True)
    slug = fields.AutoSlugField(_("Slug"), max_length=128, unique=True, populate_from="name")
    description = models.TextField(blank=True)
    destination_type = models.CharField(blank=True, max_length=12, choices=DESTINATION_TYPE_CHOICES)
    destination_id = models.IntegerField(blank=True, default=0, null=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'offer'
        db_table = 'offer_range_destination'
        verbose_name = _('Destination Range')
        verbose_name_plural = _('Destination Ranges')

    @property
    def destination_type_name(self):

        if self.destination_type == STATE:
            return "Province"
        elif self.destination_type == DISTRICT:
            return "District"
        elif self.destination_type == SUBDISTRICT:
            return "Subdistrict"
        elif self.destination_type == VILLAGE:
            return "Village"
        elif self.destination_type == ALLAREA:
            return "All Area"


class Benefit(CoreAbstractBenefit):
    range = models.ForeignKey(
        'offer.Range',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Range"))


class Condition(CoreAbstractCondition):
    range_destination = models.ForeignKey(
        "offer.RangeDestination",
        blank=True,
        default=None,
        null=True,
        on_delete=models.CASCADE
    )

    range = models.ForeignKey(
        'offer.Range',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Range"))


class Range(CoreAbstractRange):
    def add_product(self, product, display_order=None):
        """ Add product to the range
        When adding product that is already in the range, prevent re-adding it.
        If display_order is specified, update it.
        Default display_order for a new product in the range is 0; this puts
        the product at the top of the list.
        """
        initial_order = display_order or 0
        RangeProduct = get_model('offer', 'RangeProduct')
        product_model = get_model("catalogue", "Product")
        relation, __ = RangeProduct.objects.get_or_create(
            range=self, product=product,
            defaults={'display_order': initial_order})
        if product.is_parent:
            product_child = product_model.objects.filter(parent=product)
            for child in product_child:
                RangeProduct.objects.get_or_create(
                    range=self, product=child,
                    defaults={'display_order': initial_order})
        elif product.is_child:
            RangeProduct.objects.get_or_create(
                range=self, product=product.parent,
                defaults={'display_order': initial_order})
        if (display_order is not None and
            relation.display_order != display_order):
            relation.display_order = display_order
            relation.save()
        # Remove product from excluded products if it was removed earlier and
        # re-added again, thus it returns back to the range product list.
        if product.id in self._excluded_product_ids():
            self.excluded_products.remove(product)
            self.invalidate_cached_ids()

    def remove_product(self, product):
        """
        Remove product from range. To save on queries, this function does not
        check if the product is in fact in the range.
        """
        RangeProduct = get_model('offer', 'RangeProduct')
        product_model = get_model("catalogue", "Product")
        if product.is_parent:
            RangeProduct.objects.filter(range=self, product__in=product_model.objects.filter(parent=product)).delete()
        elif product.is_child:
            if len(RangeProduct.objects.filter(range=self,
                                               product__in=product_model.objects.filter(parent=product.parent))) == 1:
                RangeProduct.objects.filter(range=self, product=product.parent).delete()
        RangeProduct.objects.filter(range=self, product=product).delete()
        # Making sure product will be excluded from range products list by adding to
        # respective field. Otherwise, it could be included as a product from included
        # category or etc.
        self.excluded_products.add(product)
        # Invalidating cached property value with list of IDs of already excluded products.
        self.invalidate_cached_ids()

    def all_products(self):
        """
        Return a queryset containing all the products in the range

        This includes included_products plus the products contained in the
        included classes and categories, minus the products in
        excluded_products and parent products.
        """
        if self.proxy:
            return self.proxy.all_products()

        product_model = get_model("catalogue", "Product")
        if self.includes_all_products:
            # Filter out child products
            return product_model.browsable.all()

        return product_model.objects.filter(
            Q(id__in=self._included_product_ids()) |
            Q(product_class_id__in=self._class_ids()) |
            Q(productcategory__category_id__in=self._category_ids())
        ).exclude(
            Q(id__in=self._excluded_product_ids())
        ).distinct()


from oscar.apps.offer.models import *  # noqa isort:skip
