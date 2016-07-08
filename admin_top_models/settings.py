from django.conf import settings

SPACER_NAME = getattr(settings, 'ADMIN_TOP_MODELS_SPACER_NAME', '-' * 20)

INSERT_SPACER = getattr(settings, 'ADMIN_TOP_MODELS_INSERT_SPACER', True)

"""
ADMIN_TOP_MODELS_CONFIG = (
    ('firstapp', ('FirstModel', 'SecondModel')),
    ('secondapp', ('AModel', 'BModel', 'CModel')),
    ('thirdapp',),
)
"""
CONFIG = getattr(settings, 'ADMIN_TOP_MODELS_CONFIG', tuple())

# if this is set to True, order of apps and models will be the same across different languages,
# otherwise django's order by translated names will be used.
ALWAYS_SORT_BY_OBJECT_NAME = getattr(settings, 'ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME', False)
