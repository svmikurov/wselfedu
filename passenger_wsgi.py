# -*- coding: utf-8 -*-
import os, sys      # noqa: E401
sys.path.insert(0, '/home/d/d45400kr/wselfedu/')
sys.path.insert(1, '/home/d/d45400kr/wselfedu/.venv-beget/lib/python3.10/site-packages/')     # noqa: E501
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
from django.core.wsgi import get_wsgi_application   # noqa: E402
application = get_wsgi_application()
