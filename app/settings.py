import os

IS_PRODUCTION = os.environ.get('IS_PRODUCTION')

# if IS_PRODUCTION:
#     from .conf.production.settings import *
# else:
#     from .conf.development.settings import *

from .conf.development.settings import *

# import warnings
# from django.utils.deprecation import RemovedInDjango40Warning

# if DEBUG:
#     warnings.simplefilter('ignore', category=RemovedInDjango40Warning)
