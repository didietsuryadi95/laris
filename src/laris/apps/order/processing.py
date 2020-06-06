from oscar.apps.order.processing import EventHandler as OriginalEventHandler
from apps.partner_api.tasks import send_email_order
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from oscar.core.loading import get_model

from apps.order.models import STATUS_SHIPPED, STATUS_CANCELED

OrderNote = get_model('order', 'OrderNote')
OrderReport = get_model('order', 'OrderReport')


class EventHandler(OriginalEventHandler):

    def handle_order_status_change(self, order, new_status, note_msg=None):
        """
        Handle a requested order status change

        This method is not normally called directly by client code.  The main
        use-case is when an order is cancelled, which in some ways could be
        viewed as a shipping event affecting all lines.
        """

        old_status = order.status
        new_status = new_status
        order.set_status(new_status)
        msg = _("Order status changed from '%(old_status)s' to"
                " '%(new_status)s'") % {'old_status': old_status,
                                        'new_status': new_status}
        if note_msg:
            msg = note_msg

        for line in order.lines.all():
            line.set_status(new_status)

        if new_status in getattr(settings, 'REPLACEMENT_STOCK_STATUS'):
            self.update_stock_records(old_status, new_status, order.basket.all_lines())

        if new_status == settings.ORDER_STATUS_PAID:
            self.create_order_report(order)

        self.create_note(order, msg, old_status)
        send_email_order.delay(new_status, order.id)

    def create_note(self, order, message, old_status, note_type=OrderNote.SYSTEM):
        return order.notes.create(
            message=message, note_type=note_type, user=self.user,
            old_status=old_status, new_status=order.status)

    def update_stock_records(self, old_status, new_status, lines):
        if new_status == STATUS_SHIPPED:
            for line in lines:
                line.stockrecord.consume_allocation(line.quantity)
        elif new_status == STATUS_CANCELED:
            if old_status == STATUS_SHIPPED:
                for line in lines:
                    line.stockrecord.cancel_allocation_shipping(line.quantity)
            else:
                for line in lines:
                    line.stockrecord.cancel_allocation(line.quantity)

    def create_order_report(self, order):
        voucher = order.voucher
        if voucher:
            product_promo = voucher.amount if voucher.category != settings.ORDER_STATUS_SHIPPED else 0
        else:
            product_promo = 0
        order_report = OrderReport(
            order=order,
            number=order.number,
            order_amount=order.total_before_voucher,
            shipping_cost=order.kgx_fee,
            product_promo=product_promo,
            shipping_promo=order.shipping_discounts.last().amount if order.shipping_discounts else 0,
            total_order=order.total_incl_tax,
            source_type=order.sources.last().source_type,
            payment_method=order.sources.last().source_type.name,
            percent_fee=order.sources.last().source_type.percent_fee,
            gdn_percent_fee=order.sources.last().source_type.gdn_percent_fee,
            bank_fee=order.sources.last().source_type.bank_fee,
            gdn_bank_fee=order.sources.last().source_type.gdn_bank_fee,
            amount_fee=order.sources.last().source_type.amount_fee,
            gdn_amount_fee=order.sources.last().source_type.gdn_amount_fee,
            ipay_cost=order.ipay_cost,
            tax_vat=order.tax_vat,
            tax_pph23=order.tax_pph23,
            total_ipay_cost=order.total_ipay_cost,
            gdn_fee_percent=order.gdn_fee,
            total_gdn_fee=order.total_gdn_fee,
            income_ipay=order.total_income,
            date_placed=order.date_placed
        )
        order_report.save()
