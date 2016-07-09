=======================
django-admin-top-models
=======================


.. image:: https://img.shields.io/pypi/dm/django-admin-top-models.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-admin-top-models/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-admin-top-models.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-admin-top-models/
    :alt: Latest Version

.. image:: https://img.shields.io/travis/KostyaEsmukov/django-admin-top-models.svg?style=flat-square
    :target: https://travis-ci.org/KostyaEsmukov/django-admin-top-models
    :alt: Travis-ci

.. image:: https://img.shields.io/coveralls/KostyaEsmukov/django-admin-top-models.svg?style=flat-square
    :target: https://coveralls.io/github/KostyaEsmukov/django-admin-top-models
    :alt: Coveralls

.. image:: https://img.shields.io/github/license/KostyaEsmukov/django-admin-top-models.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-admin-top-models/
    :alt: License


Put most used and important models to the top of your Django admin index.

.. image:: https://cloud.githubusercontent.com/assets/2418596/16707176/8b4f1a28-45ce-11e6-991a-01e17d7d5ba8.png

INSTALL
-------

::

    pip install django-admin-top-models


Configuration
-------------


1. Add ``admin_top_models`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'admin_top_models',
        ...
    )


2. Add ``admin_top_models.middleware.AdminTopModelsMiddleware`` to ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        ...
        'admin_top_models.middleware.AdminTopModelsMiddleware',
        ...
    )

3. Add ``ADMIN_TOP_MODELS_CONFIG`` setting to your settings.py::

    ADMIN_TOP_MODELS_CONFIG = (
        ('firstapp', ('First', 'Third')),
        ('secondapp', ('DModel', 'CModel', 'AModel')),
        ('auth',),
    )

4. Adjust other options (if you need to. These are defaults)::

    # should the '--------------------' spacer be added between your top and the rest models?
    ADMIN_TOP_MODELS_INSERT_SPACER = True

    ADMIN_TOP_MODELS_SPACER_NAME = '-' * 20

    # if this is set to True, order of apps and models will be the same across different languages,
    # otherwise django's order by translated names will be used.
    ADMIN_TOP_MODELS_ALWAYS_SORT_BY_OBJECT_NAME = False

