from os import environ

from .base import *
ENV = environ.get('DJANGO_ENV', 'dev')

if ENV == 'dev':
    from .dev import *
else:
    from .prod import *
