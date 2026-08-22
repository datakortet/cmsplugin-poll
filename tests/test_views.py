from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cmsplugin_poll.models import Choice, Poll


class PollViewTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(question='Your choice?', pub_date=timezone.now())
        self.choice = Choice.objects.create(poll=self.poll, choice='A fine choice')

    def test_index_lists_available_polls(self):
        response = self.client.get(reverse('cmsplugin_poll:index'))

        assert response.status_code == 200
        self.assertContains(response, self.poll.question)

    def test_detail_renders_a_namespaced_vote_url(self):
        response = self.client.get(self.poll.get_absolute_url())

        assert response.status_code == 200
        self.assertContains(response, reverse('cmsplugin_poll:vote', args=[self.poll.id]))
        self.assertContains(response, 'A fine choice')

    def test_vote_increments_choice_and_marks_session(self):
        response = self.client.post(
            reverse('cmsplugin_poll:vote', args=[self.poll.id]),
            {'choice': self.choice.id},
        )

        assert response.status_code == 302
        assert response.url == self.poll.get_absolute_url()
        self.choice.refresh_from_db()
        assert self.choice.votes == 1
        assert self.client.session['poll_%d' % self.poll.id] is True

    def test_session_cannot_vote_twice(self):
        vote_url = reverse('cmsplugin_poll:vote', args=[self.poll.id])
        self.client.post(vote_url, {'choice': self.choice.id})
        response = self.client.post(vote_url, {'choice': self.choice.id})

        self.choice.refresh_from_db()
        assert self.choice.votes == 1
        response_messages = ' '.join(
            str(message) for message in get_messages(response.wsgi_request)
        )
        assert 'already vote' in response_messages

    def test_closed_poll_rejects_vote(self):
        self.poll.close_date = timezone.now()
        self.poll.save(update_fields=['close_date'])

        response = self.client.post(
            reverse('cmsplugin_poll:vote', args=[self.poll.id]),
            {'choice': self.choice.id},
        )

        self.choice.refresh_from_db()
        assert self.choice.votes == 0
        assert 'closed' in ' '.join(str(message) for message in get_messages(response.wsgi_request))

    def test_missing_choice_is_reported_without_recording_vote(self):
        response = self.client.post(reverse('cmsplugin_poll:vote', args=[self.poll.id]), {})

        self.choice.refresh_from_db()
        assert self.choice.votes == 0
        assert "didn't select" in ' '.join(
            str(message) for message in get_messages(response.wsgi_request)
        )

    def test_results_render_singular_and_plural_vote_labels(self):
        self.choice.votes = 1
        self.choice.save(update_fields=['votes'])
        Choice.objects.create(poll=self.poll, choice='Another choice', votes=2)

        response = self.client.get(reverse('cmsplugin_poll:results', args=[self.poll.id]))

        assert response.status_code == 200
        rendered = ' '.join(response.content.decode().split())
        assert '1 vote,' in rendered
        assert '2 votes,' in rendered
