DEBUG = False

try:
    from .settings import *
except ImportError:
    pass

if not DEBUG:
    import django_heroku
    django_heroku.settings(locals())
