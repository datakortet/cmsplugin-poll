from django.test import TestCase
from django.utils import timezone

from cmsplugin_poll.admin import make_closed
from cmsplugin_poll.models import Poll


class PollAdminActionTests(TestCase):
    def test_make_closed_updates_every_selected_poll(self):
        polls = [
            Poll.objects.create(question='First', pub_date=timezone.now()),
            Poll.objects.create(question='Second', pub_date=timezone.now()),
        ]

        make_closed(None, None, Poll.objects.filter(id__in=[poll.id for poll in polls]))

        assert not Poll.objects.filter(id__in=[poll.id for poll in polls], close_date=None).exists()
