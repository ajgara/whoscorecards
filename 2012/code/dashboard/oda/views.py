from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string

def scorecard_front(request, template_name="oda/scorecard_front.html", extra_context=None):
    extra_context = extra_context or {}
    extra_context["svg"] = render_to_string("oda/front.svg")
    return direct_to_template(request, template=template_name, extra_context=extra_context)

