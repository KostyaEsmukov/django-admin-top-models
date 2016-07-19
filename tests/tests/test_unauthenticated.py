
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponse
from django.template.response import TemplateResponse

from .base import BaseMiddlewareTests


class MiddlewareUnauthenticatedTests(BaseMiddlewareTests):
    def test_not_found_is_unaffected(self):
        response = self.client.get('/aaahfdkfhaldskfh')

        self.assertTrue(isinstance(response, HttpResponseNotFound))
        self.assertFalse(hasattr(response, 'context_data'))

    def test_empty_view_is_unaffected(self):
        response = self.client.get(reverse('empty_view'))

        self.assertTrue(isinstance(response, HttpResponse))
        self.assertFalse(hasattr(response, 'context_data'))

    def test_empty_template_view_is_unaffected(self):
        response = self.client.get(reverse('empty_template_view'))

        self.assertTrue(isinstance(response, TemplateResponse))
        self.assertEqual(response.context_data, dict(view=response.context_data['view']))

    def test_empty_admin_is_unaffected(self):
        response = self.client.get(reverse('admin:index'))

        self.assertTrue(isinstance(response, HttpResponse))
        self.assertTrue(not hasattr(response, 'context_data') or 'app_list' not in response.context_data)
