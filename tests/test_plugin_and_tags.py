from django.test import RequestFactory, TestCase
from django.utils import timezone

from cmsplugin_poll.cms_plugins import CMSPollPlugin
from cmsplugin_poll.models import Choice, Poll, PollPlugin
from cmsplugin_poll.templatetags.poll_tags import (
    get_choice_rate,
    get_latest_polls,
    show_results,
)


class PollPluginTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(question='A poll', pub_date=timezone.now())

    def test_render_exposes_poll_and_open_voting_state(self):
        request = RequestFactory().get('/')
        request.session = {}

        context = CMSPollPlugin().render(
            {'request': request},
            PollPlugin(poll=self.poll),
            placeholder=None,
        )

        assert context['poll'] == self.poll
        assert context['session_has_voted'] is False

    def test_render_hides_form_after_session_vote(self):
        request = RequestFactory().get('/')
        request.session = {'poll_%d' % self.poll.id: True}

        context = CMSPollPlugin().render(
            {'request': request},
            PollPlugin(poll=self.poll),
            placeholder=None,
        )

        assert context['session_has_voted'] is True


class PollTagTests(TestCase):
    def test_latest_polls_honors_requested_count(self):
        for number in range(3):
            Poll.objects.create(
                question='Poll %d' % number,
                pub_date=timezone.now() + timezone.timedelta(minutes=number),
            )

        rendered = get_latest_polls(2)

        assert 'Poll 2' in rendered
        assert 'Poll 1' in rendered
        assert 'Poll 0' not in rendered

    def test_choice_rate_is_formatted_as_a_percentage(self):
        poll = Poll.objects.create(question='Rates', pub_date=timezone.now())
        choice = Choice.objects.create(poll=poll, choice='Yes', votes=1)

        assert get_choice_rate(poll, choice) == '100%'

    def test_results_are_shown_for_voted_or_closed_polls(self):
        poll = Poll.objects.create(question='State', pub_date=timezone.now())

        assert show_results(False, poll) is False
        assert show_results(True, poll) is True

        poll.close_date = timezone.now()
        assert show_results(False, poll) is True
