from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cmsplugin_poll.models import Choice, Poll, PollPlugin


class PollModelTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question='Which foundation?',
            pub_date=timezone.now(),
        )

    def test_string_representations(self):
        choice = Choice.objects.create(
            poll=self.poll,
            choice='The original implementation',
        )
        plugin = PollPlugin(poll=self.poll)

        assert str(self.poll) == 'Which foundation?'
        assert str(choice) == 'The original implementation (Which foundation?)'
        assert str(plugin) == 'Which foundation?'

    def test_votes_and_rates(self):
        first = Choice.objects.create(poll=self.poll, choice='One', votes=3)
        second = Choice.objects.create(poll=self.poll, choice='Two', votes=1)

        assert self.poll.votes == 4
        assert self.poll.getrate(first) == 75.0
        assert self.poll.getrate(second) == 25.0

    def test_empty_poll_has_no_vote_total_or_rate(self):
        choice = Choice.objects.create(poll=self.poll, choice='No votes yet')

        assert self.poll.votes == 0
        assert self.poll.getrate(choice) == 0

    def test_absolute_url_uses_application_namespace(self):
        assert self.poll.get_absolute_url() == reverse(
            'cmsplugin_poll:poll_detail',
            kwargs={'poll_id': self.poll.id},
        )

    def test_polls_are_ordered_newest_first(self):
        newer = Poll.objects.create(
            question='A newer poll',
            pub_date=self.poll.pub_date + timezone.timedelta(days=1),
        )

        assert list(Poll.objects.values_list('id', flat=True)) == [
            newer.id,
            self.poll.id,
        ]
