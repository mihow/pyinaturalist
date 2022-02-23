# flake8: noqa: F401, F403
from logging import getLogger

logger = getLogger('pyinaturalist')
__version__ = '0.17.0'

# Ignore ImportErrors if this is imported outside a virtualenv
try:
    from pyinaturalist.auth import get_access_token
    from pyinaturalist.client import iNatClient
    from pyinaturalist.constants import *
    from pyinaturalist.formatters import enable_logging, format_table, pprint
    from pyinaturalist.models import *
    from pyinaturalist.paginator import Paginator, IDPaginator
    from pyinaturalist.request_params import get_interval_ranges
    from pyinaturalist.session import ClientSession
    from pyinaturalist.v0 import *
    from pyinaturalist.v1 import *
    from pyinaturalist.v2 import *

    # For disambiguation
    from pyinaturalist.v0 import create_observation as create_observation_v0
    from pyinaturalist.v0 import get_observations as get_observations_v0
    from pyinaturalist.v0 import update_observation as update_observation_v0
    from pyinaturalist.v0 import delete_observation as delete_observation_v0
except ImportError as e:
    logger.warning(e, exc_info=True)
