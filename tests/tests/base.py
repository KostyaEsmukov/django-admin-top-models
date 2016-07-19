
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
