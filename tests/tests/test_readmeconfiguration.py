from django.core.urlresolvers import reverse, get_urlconf, clear_url_caches
from django.contrib.admin import site
from django.test import modify_settings, override_settings

from tests.utils import reload_importlib_module
from .base import AssertIsSubsetMixin, SuperuserMixin, BaseMiddlewareTests
from .readmeconfiguration.firstapp import models as firstapp_models
from .readmeconfiguration.secondapp import models as secondapp_models
from .readmeconfiguration.thirdapp import models as thirdapp_models


@modify_settings(INSTALLED_APPS={
    'append': [
        'tests.tests.readmeconfiguration.firstapp',
        'tests.tests.readmeconfiguration.secondapp',
        'tests.tests.readmeconfiguration.thirdapp',
    ],
})
class WithReadmeConfigurationTests(AssertIsSubsetMixin, SuperuserMixin, BaseMiddlewareTests):
    app_models_modules = (firstapp_models, secondapp_models, thirdapp_models)

    spacer_name = 'jSAHDhjkshkshaduysAHDGusad'

    def setUp(self):
        super(WithReadmeConfigurationTests, self).setUp()

        for app_models_module in self.app_models_modules:
            for model_name in app_models_module.__all__:
                site.register(getattr(app_models_module, model_name))

        # reset urlresolvers cache in order to update
        # urlpatterns provided by adminsite, to include
        # the just registered models
        if get_urlconf():
            reload_importlib_module(get_urlconf())
        clear_url_caches()

    def tearDown(self):
        for app_models_module in self.app_models_modules:
            for model_name in app_models_module.__all__:
                site.unregister(getattr(app_models_module, model_name))

        if get_urlconf():
            reload_importlib_module(get_urlconf())
        clear_url_caches()

        super(WithReadmeConfigurationTests, self).tearDown()

    @override_settings(
        ADMIN_TOP_MODELS_CONFIG=(
            ('firstapp', ('First', 'Third')),
            ('secondapp', ('DModel', 'CModel', 'AModel')),
            ('auth',),
        ),
        ADMIN_TOP_MODELS_INSERT_SPACER=True,
        ADMIN_TOP_MODELS_SPACER_NAME=spacer_name,
        ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME=False
    )
    def test_readme_configuration(self):

        response = self.client.get(reverse('admin:index'))

        self.assertIsSubset([
            {'app_label': 'firstapp', 'models': [
                {'object_name': 'First'},
                {'object_name': 'Third'},
                {'object_name': 'type', 'name': self.spacer_name},
                {'object_name': 'Fourth'},
                {'object_name': 'Sixth'},
                {'object_name': 'Second'},
            ]},
            {'app_label': 'secondapp', 'models': [
                {'object_name': 'DModel'},
                {'object_name': 'CModel'},
                {'object_name': 'AModel'},
                {'object_name': 'type', 'name': self.spacer_name},
                {'object_name': 'BModel'},
                {'object_name': 'EModel'},
            ]},
            {'app_label': 'auth', 'models': [
                {'object_name': 'Group'},
                {'object_name': 'User'},
            ]},
            {'app_label': 'thirdapp', 'models': [
                {'object_name': 'Bar'},
                {'object_name': 'Foo'},
            ]},
        ], response.context_data['app_list'])

    @override_settings(
        ADMIN_TOP_MODELS_CONFIG=(
            ('firstapp', []),
            ('secondapp', ('AModel', 'BModel', 'CModel', 'DModel', 'EModel')),
            ('auth',),
        ),
        ADMIN_TOP_MODELS_INSERT_SPACER=True,
        SPACER_NAME=spacer_name,
        ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME=False
    )
    def test_spacer_not_inserted_on_edge_postions(self):

        response = self.client.get(reverse('admin:index'))

        self.assertIsSubset([
            {'app_label': 'firstapp', 'models': [
                {'object_name': 'Fourth'},
                {'object_name': 'Sixth'},
                {'object_name': 'Third'},
                {'object_name': 'Second'},
                {'object_name': 'First'},
            ]},
            {'app_label': 'secondapp', 'models': [
                {'object_name': 'AModel'},
                {'object_name': 'BModel'},
                {'object_name': 'CModel'},
                {'object_name': 'DModel'},
                {'object_name': 'EModel'},
            ]},
            {'app_label': 'auth', 'models': [
                {'object_name': 'Group'},
                {'object_name': 'User'},
            ]},
            {'app_label': 'thirdapp', 'models': [
                {'object_name': 'Bar'},
                {'object_name': 'Foo'},
            ]},
        ], response.context_data['app_list'])

    @override_settings(
        ADMIN_TOP_MODELS_CONFIG=(
            ('firstapp', ('First', 'Third')),
            ('secondapp', ('DModel', 'CModel', 'AModel')),
            ('auth',),
        ),
        ADMIN_TOP_MODELS_INSERT_SPACER=True,
        ADMIN_TOP_MODELS_SPACER_NAME=spacer_name,
        ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME=True
    )
    def test_readme_configuration_with_sort_by_object_name(self):

        response = self.client.get(reverse('admin:index'))

        self.assertIsSubset([
            {'app_label': 'firstapp', 'models': [
                {'object_name': 'First'},
                {'object_name': 'Third'},
                {'object_name': 'type', 'name': self.spacer_name},
                {'object_name': 'Fourth'},
                {'object_name': 'Second'},
                {'object_name': 'Sixth'},
            ]},
            {'app_label': 'secondapp', 'models': [
                {'object_name': 'DModel'},
                {'object_name': 'CModel'},
                {'object_name': 'AModel'},
                {'object_name': 'type', 'name': self.spacer_name},
                {'object_name': 'BModel'},
                {'object_name': 'EModel'},
            ]},
            {'app_label': 'auth', 'models': [
                {'object_name': 'Group'},
                {'object_name': 'User'},
            ]},
            {'app_label': 'thirdapp', 'models': [
                {'object_name': 'Bar'},
                {'object_name': 'Foo'},
            ]},
        ], response.context_data['app_list'])
