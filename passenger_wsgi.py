# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/d/d45400kr/wselfedu/')
sys.path.insert(1, '/home/d/d45400kr/wselfedu/venv_wselfedu/lib/python3.10/site-packages/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
