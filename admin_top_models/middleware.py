from functools import cmp_to_key

from django.core.urlresolvers import resolve

from admin_top_models.utils import list_get_or_default
from .settings import settings


class AdminTopModelsMiddleware(object):
    def process_template_response(self, request, response):
        url = resolve(request.path)

        if not url.app_name == 'admin' or url.url_name not in ('index', 'app_list'):
            return response

        try:
            response.context_data['app_list'] = self.get_reordered_app_list(response.context_data['app_list'])
        except KeyError:  # pragma: no cover
            pass

        return response

    def get_reordered_app_list(self, app_list):
        for app in app_list:
            self.reorder_models_within_app(app)

        return sorted(app_list, key=cmp_to_key(self.cmp_apps))

    def reorder_models_within_app(self, app):
        app_label = app['app_label']

        if app_label in self.config_apps_indexes_dict:
            app['models'] = sorted(app['models'], key=cmp_to_key(self.get_cmp_models(app_label)))

            if settings.INSERT_SPACER:
                self.insert_spacer_if_not_redundant(app_label, app['models'])

    def count_config_models_present_in_app_models(self, app_label, models):
        return sum(1 for model in models if model['object_name'] in self.config_app_to_models_indexesdict[app_label])

    def insert_spacer_if_not_redundant(self, app_label, models):
        idx = self.count_config_models_present_in_app_models(app_label, models)
        if 0 < idx < len(models):
            models.insert(idx, self.spacer_model_dict())

    @classmethod
    def spacer_model_dict(cls):
        # https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#django.contrib.admin.AdminSite.each_context
        return {
            'object_name': 'type',
            'name': settings.SPACER_NAME,
            'perms': {'add': False, 'change': False, 'delete': False},
            'admin_url': 'javascript://'
        }

    def cmp_apps(self, a, b):
        """
        Comparator for sorting apps in a response context.

        Puts apps defined in the ADMIN_TOP_MODELS_CONFIG to the beginning of a list
        in the order they're in the config. Other apps' order depends on ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME.

        :param a:
        :param b:
        :return:
        """
        return self.cmp_top(a['app_label'], b['app_label'], self.config_apps_indexes_dict)

    def get_cmp_models(self, app_label):
        """
        Returns a comparator for sorting models within apps.

        Puts models defined in the ADMIN_TOP_MODELS_CONFIG to the beginning of a list
        in the order they're in the config. Other models' order depends on ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME.

        :param app_name:
        :return:
        """
        return lambda a, b: self.cmp_top(a['object_name'], b['object_name'],
                                         self.config_app_to_models_indexesdict[app_label])

    @property  # not the cached_property, because settings are getting changed in the tests
    def config_apps_indexes_dict(self):
        return {app_label__models[0]: idx for idx, app_label__models in enumerate(settings.CONFIG)}

    @property  # not the cached_property, because settings are getting changed in the tests
    def config_app_to_models_indexesdict(self):
        return {app_label__models[0]: ({model: idx for idx, model in enumerate(list_get_or_default(app_label__models, 1, tuple()))})
                for app_label__models in settings.CONFIG}

    @classmethod
    def cmp_top(cls, keyA, keyB, commonIndexesDict):
        keyAin = keyA in commonIndexesDict
        keyBin = keyB in commonIndexesDict

        # both are either top or not
        if keyAin == keyBin:
            if keyAin:
                # both are top - use order from the config
                return commonIndexesDict[keyA] - commonIndexesDict[keyB]
            else:
                # both are not top
                if settings.ALWAYS_SORT_BY_OBJECT_NAME:
                    return cls.cmp_str_asc(keyA, keyB)
                else:
                    return 0  # preserve order

        # one is top, other is not
        if keyAin:
            return -1
        else:
            return 1

    @staticmethod
    def cmp_str_asc(a, b):
        # simple ascending comparator for two strings

        if a == b:  # pragma: no cover
            return 0

        if a < b:
            return -1

        return 1
