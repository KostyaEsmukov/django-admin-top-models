from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^empty_view$', views.empty_view, name='empty_view'),
    url(r'^empty_template_view$', views.EmptyTemplateView.as_view(), name='empty_template_view')
]
