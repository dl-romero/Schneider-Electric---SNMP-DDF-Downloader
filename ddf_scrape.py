
import requests
import json
import os

def get_ddf_list():
    """Gets the SNMP DDF List in JSON from SE."""
    url = "https://ddf.ecostruxureit.com/ddfsearchapi/ddfSearch?search=*snmp*&size=9999&startingIndex=0"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if os.path.isfile('ddf_files/ddf_manifest.json'):
        open('ddf_files/ddf_manifest_upgrade.json', 'wb').write(response.content)
    else:
        open('ddf_files/ddf_manifest.json', 'wb').write(response.content)
    return response.text

def download_ddf(ddf_id, ddf_filename, ddf_state):
    url = "https://ddf.ecostruxureit.com/ddfsearchapi/ddf/" + str(ddf_id) + "/download"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=True)
    if not os.path.exists('ddf_files/' + str(ddf_state).lower()):
        os.makedirs('ddf_files/' + str(ddf_state).lower())
        open('ddf_files/' + str(ddf_state).lower() + '/' + str(ddf_filename), 'wb').write(response.content)
    else:
        open('ddf_files/' + str(ddf_state).lower() + '/' + str(ddf_filename), 'wb').write(response.content)
        
def process_new():
    """Downloads the complete DDF set."""
    ddf_list = json.loads(get_ddf_list())
    for ddf in ddf_list:
        ddf_id = ddf['id']
        ddf_filename = ddf['fileName']
        ddf_filepath = ddf['filePath']
        ddf_name = ddf['ddfName']
        ddf_ddfid = ddf['ddfId']
        ddf_version = ddf['ddfVersion']
        ddf_models = ddf['models']
        ddf_vendors = ddf['vendors']
        ddf_device_types = ddf['deviceTypes']
        ddf_type = ddf['ddfType']
        ddf_state = ddf['ddfState']
        download_ddf(ddf_id, ddf_filename, ddf_state)
        
def process_upgrade():
    """Upgrades DDF Files based on Version."""
    ddf_list = json.loads(get_ddf_list())
    for ddf in ddf_list:
        ddf_id = ddf['id']
        ddf_filename = ddf['fileName']
        ddf_filepath = ddf['filePath']
        ddf_name = ddf['ddfName']
        ddf_ddfid = ddf['ddfId']
        ddf_version = ddf['ddfVersion']
        ddf_models = ddf['models']
        ddf_vendors = ddf['vendors']
        ddf_device_types = ddf['deviceTypes']
        ddf_type = ddf['ddfType']
        ddf_state = ddf['ddfState']
        download_ddf(ddf_id, ddf_filename, ddf_state)
    os.remove("ddf_manifest.json")
    os.rename('ddf_manifest_upgrade.json','ddf_manifest.json') 

if __name__ == "__main__":
    if not os.path.exists('ddf_files'):
        os.makedirs('ddf_files')
    if os.path.isfile('ddf_files/ddf_manifest.json'):
        process_upgrade()
    else:
        process_new()