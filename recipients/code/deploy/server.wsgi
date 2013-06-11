import os, sys

# activate virtualenv
activate_this = os.path.expanduser("~/.virtualenvs/who2012/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

# tell django where our settings module is
sys.path.insert(0, os.path.expanduser("~/repos/who/2012/code/"))
sys.path.insert(0, os.path.expanduser("~/repos/who/2012/code/dashboard"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings_prod'

# run django
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
