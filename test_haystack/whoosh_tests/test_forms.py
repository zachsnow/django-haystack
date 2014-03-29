# encoding: utf-8
from __future__ import absolute_import

from django.conf import settings
from django.http import HttpRequest
from mock import patch

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

from .test_whoosh_backend import LiveWhooshRoundTripTestCase


@patch.dict(settings.HAYSTACK_CONNECTIONS['whoosh'], {'INCLUDE_SPELLING': True})
class SpellingSuggestionTestCase(LiveWhooshRoundTripTestCase):
    def test_form_suggestion(self):
        form = SearchForm({'q': 'exampl'}, searchqueryset=SearchQuerySet('whoosh'))
        self.assertEqual(form.get_suggestion(), 'example')

    def test_view_suggestion(self):
        view = SearchView(template='test_suggestion.html', searchqueryset=SearchQuerySet('whoosh'))
        mock = HttpRequest()
        mock.GET['q'] = 'exampl'
        resp = view(mock)
        self.assertEqual(resp.content, b'Suggestion: example')
