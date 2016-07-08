from django.http import HttpResponse
from django.views.generic import TemplateView


def empty_view(request):
    return HttpResponse('')


class EmptyTemplateView(TemplateView):
    template_name = "empty.html"
