try:
    from settings import *
except ImportError:
    import sys
    sys.stderr.write("Unable to read settings.py\n")
    sys.exit(1)

SITE_URL = '/who'
FORCE_SCRIPT_NAME = SITE_URL
STATIC_URL = '/who/static/'
