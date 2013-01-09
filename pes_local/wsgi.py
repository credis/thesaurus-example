"""
WSGI config for pes project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""


ALLDIRS = ['/home/clo/projects/pes']

# the above directory depends on the location of your python installation.
# if using virtualenv, it will need to match your projects locale.
import os
import sys
import site

prev_sys_path = list(sys.path)

for directory in ALLDIRS:
    site.addsitedir(directory)
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
            sys.path[:0] = new_sys_path


sys.path.append('/home/clo/projects/testpes/tthess')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pes_local.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

from django.core.wsgi import get_wsgi_application

# Uncomment to add sentry
try:
    from raven.contrib.django.middleware.wsgi import Sentry
    application = Sentry(get_wsgi_application())
except ImportError:
    application = get_wsgi_application()



# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.





# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
