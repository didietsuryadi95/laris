from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CampaignConfig(AppConfig):
    label = 'campaign'
    name = 'apps.campaign'
    verbose_name = _('Catalogue')

    def ready(self):
        from . import signals  # noqa
