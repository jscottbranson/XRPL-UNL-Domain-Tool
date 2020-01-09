'''
Variables for the websocket and SQL connections.
'''
import logging

LOG_LEVEL = logging.WARN
LOG_FILE = "log/unl_domain_tool.log"

# Time (in seconds) to sleep between queries.
SLEEP = 30
#Time (in seconds) to sleep before trying to recover from an error.
SLEEP_ERROR = 30

UNL_ADDRESS = "https://vl.ripple.com"

DATA_API_DOMAINS_ADDRESS = "https://data.ripple.com/v2/network/validators?format=json"

# The following address must have a validator master key appended to work properly
VALIDATOR_API_DOMAIN_ADDRESS = "https://data.ripple.com/v2/network/validators/"

DOMAIN_MAP_JSON_FILE = "domain_map.json"
