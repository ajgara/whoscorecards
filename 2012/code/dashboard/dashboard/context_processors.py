def site_url(request):
    from django.conf import settings
    return {'SITE_URL' : settings.SITE_URL }
       
