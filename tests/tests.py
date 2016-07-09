from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound, HttpResponse
from django.template.response import TemplateResponse
from django.test import TestCase, modify_settings
from django.contrib.auth.models import User


@modify_settings(MIDDLEWARE_CLASSES={
    'append': 'admin_top_models.middleware.AdminTopModelsMiddleware'
})
class BaseMiddlewareTests(TestCase):
    pass


class AssertIsSubsetMixin(object):
    def assertIsSubset(self, subset, dict_or_list, msg=None):

        def inner(subset, dict_or_list):
            if isinstance(dict_or_list, list):
                assert isinstance(subset, list)
                assert len(dict_or_list) == len(subset)

                for i in range(len(dict_or_list)):
                    inner(subset[i], dict_or_list[i])
            elif isinstance(dict_or_list, dict):
                assert isinstance(subset, dict)

                for k, _ in subset.items():
                    inner(subset[k], dict_or_list[k])
            else:
                assert subset == dict_or_list

        try:
            inner(subset, dict_or_list)
        except (AssertionError, KeyError):
            standardMsg = '%s is not a subset of %s' % (dict_or_list, subset)
            msg = self._formatMessage(msg, standardMsg)
            self.fail(msg)


class SuperuserMixin(object):
    def setUp(self):
        super(SuperuserMixin, self).setUp()

        self.superuser_password = 'secret'
        self.superuser = User.objects.create_superuser(username='super', password=self.superuser_password, email='super@example.com')
        try:
            self.client.force_login(self.superuser)
        except AttributeError:
            # force_login is introduced in Django 1.9
            # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#django.test.Client.force_login
            self.assertTrue(self.client.login(
                username=self.superuser.username,
                password=self.superuser_password
            ))


class MiddlewareWithSuperuserTests(AssertIsSubsetMixin, SuperuserMixin, BaseMiddlewareTests):
    def test_process_template_response(self):
        response = self.client.get(reverse('admin:index'))

        self.assertTrue(hasattr(response, 'context_data'))

        self.assertIsSubset([{'app_label': 'auth', 'models': [
            {'object_name': 'Group'},
            {'object_name': 'User'},
        ]}], response.context_data['app_list'])


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
