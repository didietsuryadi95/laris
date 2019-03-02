import datetime

from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_class, get_model

ReportGenerator = get_class('dashboard.reports.reports', 'ReportGenerator')
ReportCSVFormatter = get_class('dashboard.reports.reports',
                               'ReportCSVFormatter')
ReportHTMLFormatter = get_class('dashboard.reports.reports',
                                'ReportHTMLFormatter')

OrderReport = get_model('order', 'OrderReport')


class WithdrawalReportCSVFormatter(ReportCSVFormatter):
    filename_template = 'withdrawal-%s.csv'

    def generate_csv(self, response, orders):
        writer = self.get_csv_writer(response)
        header_row = [(_('Order Transaction'), 6),
                      (_('Ipay Fee'), 7),
                      (_('GDN Fee'), 1),
                      (_('KGX Fee'), 1),
                      (_('Merchant Fee'), 4)]
        arrange_row = []
        for h in header_row:
            arrange_row.append(h[0])
            for i in range(h[1]):
                arrange_row.append('')
        writer.writerow(arrange_row)
        header_row_2 = [
            _("Order number"),
            _("Order Date Placed"),
            _("Order Amount"),
            _("Shipping Cost"),
            _("Product Promo"),
            _("Shiping Promo"),
            _("Total Order"),
            _("Payment Method"),
            _("% Based"),
            _("Bank Fee"),
            _("Amount Base"),
            _("iPay Cost"),
            _("Tax for iPay (VAT)"),
            _("Service Tax (PPh23)"),
            _("Total iPay Cost"),
            _("% Based"),
            _("Total GDN Fee"),
            _("KGX Fee"),
            _("Promo Shipping"),
            _("Total Order"),
            _("Total iPay Cost"),
            _("Total GDN Cost"),
            _("Income Transferred by iPay88"),
            _("Remarks"),
        ]
        writer.writerow(header_row_2)
        for order in orders:
            row = self.get_order_row(order)
            writer.writerow(row)

        writer.writerow(['Summary'])

        total_order_before_voucher = sum([getattr(o, 'order_amount') for o in orders])
        total_order_incl_tax = sum([getattr(o, 'total_order') for o in orders])
        total_kgx_fee = sum([getattr(o, 'shipping_cost') for o in orders])
        total_ipay_cost = sum([getattr(o, 'ipay_cost') for o in orders])
        final_total_ipay_cost = sum([getattr(o, 'total_ipay_cost') for o in orders])
        total_order_gdn_fee = sum([getattr(o, 'total_gdn_fee') for o in orders])
        total_order_income_tf = sum([getattr(o, 'income_ipay') for o in orders])
        writer.writerow([
            '', '', total_order_before_voucher, total_kgx_fee, '', '', total_order_incl_tax, '', '', '', '',
            total_ipay_cost, '', '', final_total_ipay_cost, '', total_order_gdn_fee, total_kgx_fee, '',
            total_order_incl_tax, final_total_ipay_cost, total_order_gdn_fee, total_order_income_tf
        ])

    @staticmethod
    def get_order_row(order):
        return [
            order.number,
            order.date_placed,
            order.order_amount,
            order.shipping_cost,
            order.product_promo or '-',
            order.shipping_promo or '-',
            order.total_order,
            order.payment_method,
            order.total_percent_fee or '-',
            order.total_bank_fee or '-',
            order.total_amount_fee or '-',
            order.ipay_cost or '-',
            order.tax_vat or '-',
            order.tax_pph23 or '-',
            order.total_ipay_cost,
            order.gdn_fee_percent,
            order.total_gdn_fee,
            order.shipping_cost,
            order.shipping_promo or '-',
            order.total_order,
            order.total_ipay_cost or '-',
            order.total_gdn_fee,
            order.income_ipay,
            _('Include shipping cost')
        ]

    def filename(self, **kwargs):
        start_date = kwargs['start_date']
        end_date = kwargs['end_date']
        date_str = _('all')
        if start_date:
            date_str = _(f'from {start_date}')
        if end_date:
            date_str = _(f'until {end_date}')
        if start_date and end_date:
            date_str = _(f'between {start_date} and {end_date}')
        return self.filename_template % date_str


class WithdrawalReportHTMLFormatter(ReportHTMLFormatter):
    filename_template = 'dashboard/reports/partials/withdrawal_report.html'


class WithdrawalReportGenerator(ReportGenerator):
    code = 'withdrawal_report'
    description = _("Withdrawal")
    date_range_field_name = 'date_placed'

    formatters = {
        'CSV_formatter': WithdrawalReportCSVFormatter,
        'HTML_formatter': WithdrawalReportHTMLFormatter,
    }

    def generate(self):
        qs = OrderReport.objects.all().order_by('-date_placed')

        if self.start_date:
            qs = qs.filter(date_placed__gte=self.start_date)
        if self.end_date:
            qs = qs.filter(
                date_placed__lt=self.end_date + datetime.timedelta(days=1))
        if self.order_number:
            qs = qs.filter(number=self.order_number)

        additional_data = {
            'start_date': self.start_date,
            'end_date': self.end_date
        }

        return self.formatter.generate_response(qs, **additional_data)

    def is_available_to(self, user):
        return user.is_staff
