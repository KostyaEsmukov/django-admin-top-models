
from django.core.urlresolvers import reverse

from .base import AssertIsSubsetMixin, SuperuserMixin, BaseMiddlewareTests


class MiddlewareWithSuperuserTests(AssertIsSubsetMixin, SuperuserMixin, BaseMiddlewareTests):
    def test_process_template_response(self):
        response = self.client.get(reverse('admin:index'))

        self.assertTrue(hasattr(response, 'context_data'))

        self.assertIsSubset([{'app_label': 'auth', 'models': [
            {'object_name': 'Group'},
            {'object_name': 'User'},
        ]}], response.context_data['app_list'])
