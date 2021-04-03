from django.apps import AppConfig
from django.utils.translation import gettext, gettext_lazy as _

class MuniElectionConfig(AppConfig):
    name = 'muni_election'
    verbose_name = _('Municipality Election')
