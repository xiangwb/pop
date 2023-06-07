import os

if os.environ.get('DEBUG'):
    from .development import *
else:
    from .production import *
# from .test import *