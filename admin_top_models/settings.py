from django.conf import settings as django_settings


def settings_property_with_default(name, default):
    return property(lambda _: getattr(django_settings, name, default))


class AppSettings:
    """
    This class holds app-specific settings,
    which are taken (using descriptor) from
    django.conf.settings each time they're read.

    Though Django settings are meant to be immutable,
    they are getting changed while running tests,
    hence that hack with properties.
    """

    SPACER_NAME = settings_property_with_default('ADMIN_TOP_MODELS_SPACER_NAME', '-' * 20)

    INSERT_SPACER = settings_property_with_default('ADMIN_TOP_MODELS_INSERT_SPACER', True)

    """
    ADMIN_TOP_MODELS_CONFIG = (
        ('firstapp', ('FirstModel', 'SecondModel')),
        ('secondapp', ('AModel', 'BModel', 'CModel')),
        ('thirdapp',),
    )
    """
    CONFIG = settings_property_with_default('ADMIN_TOP_MODELS_CONFIG', tuple())

    # if this is set to True, order of apps and models will be the same across different languages,
    # otherwise django's order by translated names will be used.
    ALWAYS_SORT_BY_OBJECT_NAME = settings_property_with_default('ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME', False)


settings = AppSettings()
