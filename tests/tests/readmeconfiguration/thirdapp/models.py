from django.db import models

from .apps import ThirdappConfig

__all__ = ['Foo', 'Bar']


class MetaAppLabelMixin(object):
    class Meta:
        app_label = ThirdappConfig.name


class Foo(MetaAppLabelMixin, models.Model):
    pass


class Bar(MetaAppLabelMixin, models.Model):
    pass
