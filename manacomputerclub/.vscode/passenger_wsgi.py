# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/t/timk2342.beget.tech/manacomputerclub')
sys.path.insert(1, '/home/t/timk2342.beget.tech/venv_django/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'manacomputerclub.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()