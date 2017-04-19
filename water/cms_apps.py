from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class WaterApphook(CMSApp):
    app_name = "water"
    name = _("Water Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["water.urls"]


apphook_pool.register(WaterApphook)  # register the applica
