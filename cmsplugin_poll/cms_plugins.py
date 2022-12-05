from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import PollPlugin
from django.utils.translation import ugettext as _


class CMSPollPlugin(CMSPluginBase):
    model = PollPlugin
    name = _("Simple poll")
    render_template = "cmsplugin_poll/detail.html"

    def render(self, context, instance, placeholder):
        context['poll'] = instance.poll
        closed = instance.poll.close_date is not None
        voted = context['request'].session.get("poll_%d" % instance.poll.id)
        context['session_has_voted'] = voted or closed
        return context

plugin_pool.register_plugin(CMSPollPlugin)
