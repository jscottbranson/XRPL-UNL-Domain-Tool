# XRPL-UNL-Domain-Retriever
This script retrieves the master validation keys from a published UNL, then queries multiple specified API (typically the [Ripple Data API v2]) endpoints for the domains associated with the UNL keys. The purpose of querying two endpoints is simply to overcome the issue with the Data API failing to return the domain names for some validators via the `validators` endpoint.

## Required Packages
`requests` - Used to retrieve the encoded UNL
[`parse_unl`] - Used to parse published XRPL UNLs
`ecdsa` - required for `parse_unl`

## Use
This has been tested in Python version 3.7. Feedback on testing with other versions is appreciated.

The most simple way to interact with the program is to configure `variables.py` then `python run.py`.
Keyboard interrupt will exit the program.


While running, a JSON file is created with the following keys:
- `status`: Either `Error` or `Success`.
- `updated_time`: Last time the file was written to.
- `unl_lenght`: The number of validators in the specified UNL.
- `results_length`: The number of master key:domain mappings in the `mappings` dictionary.
- `mappings`: A dictionary with the 'master validation key' : 'domain' mappings.

## Known Validator List Sites
- `https://vl.ripple.com`
- `https://vl.coil.com`

## Issues
This code is hastily written to fill a few specific needs that I have, so it likely has issues. Better error handling is needed, and the script will not update the file if it fails (hence the "status" result is basically pointless).

## License
GNU GPLv3

## Contact
Visit me at [https://rabbitkick.club] or on Twitter [@xrpl_rabbit].

[Ripple Data API v2]:https://xrpl.org/data-api.html
[`parse_unl`]:https://github.com/crypticrabbit/xrpl_unl_parser
[https://rabbitkick.club]:https://rabbitkick.club
[@xrpl_rabbit]:https://twitter.com/xrpl_rabbit
