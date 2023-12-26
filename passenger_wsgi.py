# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/d/wselfedu/wselfedu')
sys.path.insert(1, '/home/d/wselfedu/venv_wselfedu/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'wselfedu.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
