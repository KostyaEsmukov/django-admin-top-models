from django.db import models

from .apps import FirstappConfig

__all__ = ['First', 'Second', 'Third', 'Fourth', 'Sixth']


class MetaAppLabelMixin(object):
    class Meta:
        app_label = FirstappConfig.name


class First(models.Model):
    class Meta(MetaAppLabelMixin.Meta):
        verbose_name = "ZFirst"


class Second(models.Model):
    class Meta(MetaAppLabelMixin.Meta):
        verbose_name = "YSecond"


class Third(MetaAppLabelMixin, models.Model):
    pass


class Fourth(MetaAppLabelMixin, models.Model):
    pass


class Sixth(MetaAppLabelMixin, models.Model):
    pass
