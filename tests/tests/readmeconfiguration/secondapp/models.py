from django.db import models

from .apps import SecondappConfig

__all__ = ['AModel', 'BModel', 'CModel', 'DModel', 'EModel']


class MetaAppLabelMixin(object):
    class Meta:
        app_label = SecondappConfig.name


class AModel(MetaAppLabelMixin, models.Model):
    pass


class BModel(MetaAppLabelMixin, models.Model):
    pass


class CModel(MetaAppLabelMixin, models.Model):
    pass


class DModel(MetaAppLabelMixin, models.Model):
    pass


class EModel(MetaAppLabelMixin, models.Model):
    pass
