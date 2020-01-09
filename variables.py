'''
Variables for the websocket and SQL connections.
'''
import logging

LOG_LEVEL = logging.WARN

UNL_ADDRESS = "https://vl.ripple.com"

DATA_API_DOMAINS_ADDRESS = "https://data.ripple.com/v2/network/validators?format=json"

# The following address must have a validator master key appended to work properly
VALIDATOR_API_DOMAIN_ADDRESS = "https://data.ripple.com/v2/network/validators/"

DOMAIN_MAP_JSON_FILE = "domain_map.json"
