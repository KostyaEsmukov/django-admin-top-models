#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django
from django.conf import settings


class DjangoTestRunner(object):
    DIRNAME = os.path.dirname(__file__)

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    ]

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    )

    def __init__(self, apps, **settings):
        self.apps = apps
        self.settings = settings

    def run(self):
        settings.configure(
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': os.path.join(self.DIRNAME, 'db.sqlite3'),
                    }
                },
                INSTALLED_APPS=self.INSTALLED_APPS + self.apps,
                MIDDLEWARE_CLASSES=self.MIDDLEWARE_CLASSES,
                SECRET_KEY='fakekey',
                **self.settings
        )

        try:
            # Django <= 1.8
            from django.test.simple import DjangoTestSuiteRunner
            test_runner = DjangoTestSuiteRunner(verbosity=1)
        except ImportError:
            # Django >= 1.8
            from django.test.runner import DiscoverRunner
            test_runner = DiscoverRunner(verbosity=1)

        if django.VERSION >= (1, 7, 0):
            # see: https://docs.djangoproject.com/en/dev/releases/1.7/#standalone-scripts
            django.setup()

        if django.VERSION >= (1, 6, 0):
            # see: https://docs.djangoproject.com/en/dev/releases/1.6/#discovery-of-tests-in-any-test-module
            from django.test.runner import DiscoverRunner as Runner
        else:
            from django.test.simple import DjangoTestSuiteRunner as Runner

        failures = Runner().run_tests(self.apps, verbosity=1)
        if failures:  # pragma: no cover
            sys.exit(failures)


if __name__ == '__main__':
    DjangoTestRunner(['admin_top_models', 'tests'], ROOT_URLCONF='tests.urls').run()
