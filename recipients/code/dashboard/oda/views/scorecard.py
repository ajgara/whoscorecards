from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def scorecard(request, iso3):
    if request.GET.get("page", "1") == "1":
        return redirect(reverse(scorecard_front, kwargs={"iso3" : iso3}))
    else:
        return redirect(reverse(scorecard_back, kwargs={"iso3" : iso3}))
