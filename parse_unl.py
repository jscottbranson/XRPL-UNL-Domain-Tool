'''
Retrieve and parse a published rippled UNL.
Returns base58 encoded XRP Ledger keys.
'''

import json
import codecs
from hashlib import sha256
from base64 import b64decode

import requests

# Verify signatures
import ecdsa


def verify_signature(**kwargs):
    '''
    Verify the UNL is properly signed.
    '''
    blob = str(kwargs['blob'])
    print(kwargs['public_key'])
    eph_key = kwargs['manifest']
    master_key = kwargs['public_key'].encode('utf-8')
    sig = codecs.encode(codecs.decode(kwargs['signature'], 'hex'), 'base64').decode()

    # manifest contains the ephemeral key, which is derived from the 'public_key'
    # manifest is serialized using ripple's serialization
    # https://github.com/ripple/ripple-dev-portal/blob/master/content/_code-samples/tx-serialization/serialize.py
    manifest = b64decode(kwargs['manifest']).decode()

    #manifest = codecs.encode(codecs.decode(unl.json()['manifest'], 'hex'), 'base64').decode()
    print(manifest)


    #vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(key), curve=ecdsa.SECP256k1)
    #vk.verify(bytes.fromhex(sig), blob)

def rippled_bs58(key):
    '''
    Returns a string that is encoded using the rippled base58 alphabet.
    '''
    alphabet = b'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz'
    string = b''
    while key:
        key, idx = divmod(key, 58)
        string = alphabet[idx:idx+1] + string
    return string

def parse_master_key(key):
    '''
    Returns a base58 encoded master public validation key.
    '''
    payload = "1C" + key
    return rippled_bs58(int(payload + sha256(bytearray.fromhex(sha256(
        bytearray.fromhex(payload)).hexdigest())).hexdigest()[0:8], 16)).decode('utf-8')

def parse_ephemeral_key(key):
    '''
    Returns a base58 encoded ephemeral validation key.
    '''
    key = key

    return ''

def unl_parser(address):
    '''
    Download the UNL and base64 decode the blob.
    Individual validation keys are then constructed from the decoded blob
    payload and the double sha256 hashed checksums. Keys are then base58 encoded.
    '''
    keys = {'status': 'Error',
            'error': False,
            'http_code': '',
            'public_validation_keys': [],
            'public_key': "",
            'expiration': '',}

    try:
        unl = requests.get(address)
        keys['http_code'] = unl.status_code
        unl.raise_for_status()

    except requests.exceptions.RequestException:
        keys['error'] = "Invalid URL: {}.".format(address)
        return json.dumps(keys)

    try:
        blob = json.loads(b64decode(unl.json()['blob']).decode('utf-8'))
        validators = blob['validators']
        keys['public_key'] = (unl.json()['public_key'])

        '''
        Convert Ripple Epoch to Unix Epoch
        Reference : https://xrpl.org/basic-data-types.html
        '''
        keys['expiration'] = blob['expiration'] + 946684800

    except json.decoder.JSONDecodeError:
        keys['error'] = "Invalid or malformed manifest."
        return json.dumps(keys)

    if not validators:
        keys['error'] = "List of validator keys was empty."
        return json.dumps(keys)

    for i in validators:
        keys['public_validation_keys'].append(
            {'master': parse_master_key(i['validation_public_key']),
             'ephemeral': parse_ephemeral_key(i['manifest'])})

    keys['status'] = 'Success'
    return json.dumps(keys)
