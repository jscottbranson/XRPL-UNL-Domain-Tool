'''
Brings all the functions together to make the code run.

'''
import sys
import time
import logging
import json

import requests

import variables
from parse_unl import unl_parser

logging.basicConfig(
    level=variables.LOG_LEVEL,
    filename=variables.LOG_FILE,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s",
)

JSON_FILE = variables.DOMAIN_MAP_JSON_FILE

def restart_program():
    '''
    Placeholder in case I want to add additional actions and/or logging when the program
    restarts.
    '''
    logging.critical("Something went wrong, and the program restarted itself. Perhaps a URL was unreachable?")
    time.sleep(variables.SLEEP_ERROR)

def retrieve_from(address):
    '''
    Return a parsed response from HTTP get request from a given address.
    '''
    try:
        response = requests.get(address).json()
    except (
            requests.exceptions.RequestException,
            json.JSONDecodeError
    ) as error:
        logging.critical(error, "Unable to retrieve domains from the Data API.")
        restart_program()

    return response

def get_unl_master_keys(master_keys):
    '''
    Use the unl_parser to retrieve and parse UNL keys and return a dict of UNL master keys.
    '''
    unl_master_keys = []
    unl = json.loads(unl_parser(variables.UNL_ADDRESS))

    for i in unl['public_validation_keys']:
        if i not in master_keys:
            master_keys.update({i: ''})
        unl_master_keys.append(i)

    # Check to see if any master validation keys were deleted, and remove those keys from the list
    for i in master_keys.keys():
        if i not in unl_master_keys:
            del master_keys[i]

    return master_keys

def get_domains(unl_master_keys):
    '''
    Use the rippled Data API to query domains associated with master keys.
    '''
    for i in unl_master_keys:
        if not unl_master_keys[i]:
            address = variables.DATA_API_DOMAINS_ADDRESS
            response = retrieve_from(address)
            try:
                response = response['validators']
            except (KeyError) as error:
                logging.critical(error, "Unexpected key in the domain list returned by the Data API.")
                restart_program()

            for l in response:
                if l['validation_public_key'] in unl_master_keys:
                    l.setdefault('domain')
                    unl_master_keys[l['validation_public_key']] = l['domain']

        else:
            pass

        return unl_master_keys

def get_individual_validator_report(domains):
    '''
    The Data API will typically store domain in the individual validator response,
    even if it isn't available from the `validators` endpoint (that was tried in the
    `get_domains` function.
    '''
    for i in domains:
        if not domains[i]:
            address = variables.VALIDATOR_API_DOMAIN_ADDRESS + i
            response = retrieve_from(address)
            domains[i] = response['domain']
    return domains

def open_json_file():
    '''
    Open a json file and return the parsed json.
    '''
    try:
        with open(JSON_FILE, "r") as data:
            file = data.read()
        try:
            file = json.loads(file)
        except (
                TypeError,
                json.JSONDecodeError):
            file = open(JSON_FILE, "w")
            file = {'mappings': {}}
    except FileNotFoundError:
        file = open(JSON_FILE, "w")
        file = {'mappings': {}}

    return file

def write_json_file(data):
    '''
    Output JSON with master key:domain mappings to a file.
    '''
    with open(JSON_FILE, 'w') as i:
        json.dump(data, i)
    return 1

def fetch_unl():
    '''
    Run the code, then sleep for a specified time before rerunning.
    '''
    keys = open_json_file()['mappings']

    try:
        unl_master_keys = get_unl_master_keys(keys)
        logging.info("Successfully retrieved master keys from the specified UNL.")
        logging.info("There are " + str(len(unl_master_keys)) + " validators in the UNL.")
    except () as error:
        logging.critical(error, "Error retrieving the UNL")
        restart_program()

    try:
        domains = get_domains(unl_master_keys)
        logging.info("Successfully retrieved the domain list from the Data API.")
    except () as error:
        logging.critical(error, "Error retrieving the domain list from the Data API.")
        restart_program()

    domains = get_individual_validator_report(domains)

    output = {
        'status': 'Success',
        'updated_time': time.time(),
        'unl_length': len(unl_master_keys),
        'results_length': len(domains),
        'mappings': domains,
    }
    write_json_file(output)

try:
    while True:
        fetch_unl()
        time.sleep(variables.SLEEP)
except KeyboardInterrupt:
    sys.exit(0)
