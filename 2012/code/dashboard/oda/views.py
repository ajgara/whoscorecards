from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from django.template import loader, Context
from django.http import HttpResponse

def scorecard_front(request, template_name="oda/scorecard_front.html", extra_context=None):
    extra_context = extra_context or {}
    return direct_to_template(request, template=template_name, extra_context=extra_context)

