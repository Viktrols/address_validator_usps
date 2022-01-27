import json
from requests import Session

from csv_converter import (convert_csv_to_list_of_dicts,
                           convert_list_of_dicts_to_csv)
from get_headers import get_random_headers


USPS_URL = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'
# I used this url I found on stackoverflow:) instead
# https://tools.usps.com/zip-code-lookup.htm?byaddress
# because it's easier, no html parsing needed and it works!

def get_payload_data(address_params: dict):
    '''
    Get the data that is needed for the query from dict with address
    '''
    payload_data = {
        'companyName': address_params.get('Company'),
        'address1':  address_params.get('Street'),
        'city':  address_params.get('City'),
        'state':  address_params.get('St'),
        'zip':  address_params.get('ZIPCode'),
        'encode': 'form',
        }
    return payload_data


def check_address(url: str, data: dict, headers: str):
    '''
    Make a post-request to usps to check the address,
    return Valid if the address exists.
    '''
    session = Session()    
    request = session.post(url=url, data=data, headers=headers)
    print(json.loads(request.text))
    result_status = json.loads(request.text)['resultStatus']
    return 'Valid' if result_status == 'SUCCESS' else 'Invalid'


def main():
    '''
    Open and convert сsv with addresses,
    for each of the addresses make a verification request,
    write the result to a new сsv file.
    '''
    headers = get_random_headers()
    list_with_addresses = convert_csv_to_list_of_dicts('input_data.csv')
    checked_addresses = []
    for address in list_with_addresses:
        payload_data = get_payload_data(address)
        is_valid = check_address(USPS_URL, payload_data, headers)
        address['Is_valid'] = is_valid
        checked_addresses.append(address)
    convert_list_of_dicts_to_csv(checked_addresses, 'output_data.csv')


if __name__ == '__main__':
    main()
