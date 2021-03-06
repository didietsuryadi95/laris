from oscar.apps.order.utils import OrderCreator as OriginalOrderCreator
from oscar.apps.order.utils import OrderNumberGenerator as OriginalOrderNumberGenerator
from oscar.apps.order import exceptions
from django.conf import settings
from oscar.core.loading import get_model

Line = get_model('order', 'Line')


class OrderCreator(OriginalOrderCreator):

    def create_line_models(self, order, basket_line, extra_line_fields=None):
        """
        Create the batch line model.

        You can set extra fields by passing a dictionary as the
        extra_line_fields value
        """
        product = basket_line.product
        stockrecord = basket_line.stockrecord
        if not stockrecord:
            raise exceptions.UnableToPlaceOrder(
                "Basket line #%d has no stockrecord" % basket_line.id)
        if len(basket_line.basket.offer_discounts) == 0:
            unit_price_excl_tax_incl_discount = basket_line.unit_price_excl_tax
            unit_price_incl_tax_incl_discount = basket_line.unit_price_incl_tax
        else:
            unit_price_excl_tax_incl_discount = basket_line.unit_price_excl_tax_incl_discount
            unit_price_incl_tax_incl_discount = basket_line.unit_price_incl_tax_incl_discount
        partner = stockrecord.partner
        line_data = {
            'order': order,
            # Partner details
            'partner': partner,
            'partner_name': partner.name,
            'partner_sku': stockrecord.partner_sku,
            'stockrecord': stockrecord,
            # Product details
            'product': product,
            'title': product.get_title(),
            'upc': product.upc,
            'quantity': basket_line.quantity,
            # Price details
            'line_price_excl_tax':
            basket_line.line_price_excl_tax_incl_discounts,
            'line_price_incl_tax':
            basket_line.line_price_incl_tax_incl_discounts,
            'line_price_after_discounts_excl_tax': unit_price_excl_tax_incl_discount,
            'line_price_after_discounts_incl_tax': unit_price_incl_tax_incl_discount,
            'line_price_before_discounts_excl_tax':
            basket_line.line_price_excl_tax,
            'line_price_before_discounts_incl_tax':
            basket_line.line_price_incl_tax,
            # Reporting details
            'unit_cost_price': stockrecord.cost_price,
            'unit_price_incl_tax': basket_line.unit_price_incl_tax,
            'unit_price_excl_tax': basket_line.unit_price_excl_tax,
            'unit_retail_price': stockrecord.price_retail,
            # Shipping details
            'est_dispatch_date':
            basket_line.purchase_info.availability.dispatch_date
        }
        extra_line_fields = extra_line_fields or {}
        if hasattr(settings, 'OSCAR_INITIAL_LINE_STATUS') and not (extra_line_fields and 'status' in extra_line_fields):
            extra_line_fields['status'] = getattr(settings, 'OSCAR_INITIAL_LINE_STATUS')
        if extra_line_fields:
            line_data.update(extra_line_fields)

        order_line = Line._default_manager.create(**line_data)
        self.create_line_price_models(order, order_line, basket_line)
        self.create_line_attributes(order, order_line, basket_line)
        self.create_additional_line_models(order, order_line, basket_line)

        return order_line


class OrderNumberGenerator(OriginalOrderNumberGenerator):

    def order_number(self, basket):
        """
        Return an order number for a given basket
        """
        return f"{getattr(settings, 'ORDER_NUMBER_PREFIX')}-{100000 + basket.id}"
