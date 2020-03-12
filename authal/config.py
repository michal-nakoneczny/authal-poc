import logging
import os


def _get_boolean_env_variable(name: str) -> bool:
    return os.getenv(name) == "true"


VERSION = "0.0.1"
LOG_LEVEL = int(os.getenv("LOG_LEVEL", logging.NOTSET))
DEFAULT_PAGE_LIMIT = 20

# always set those from outside
MONGODB_URL = os.environ["MONGODB_URL"]

ENABLE_SENTRY = _get_boolean_env_variable("ENABLE_SENTRY")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_ENV = os.getenv("SENTRY_ENV")

MONGO_MAX_POOL_SIZE = int(os.getenv("MONGO_MAX_POOL_SIZE", 100))

# ====== Feature flags ======
# ENABLE_FOO = _get_boolean_env_variable("ENABLE_FOO")
