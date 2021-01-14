import json
import os
import os.path
import requests

def get_ddf_list():
    """Gets the SNMP DDF List in JSON from SE."""
    url = "https://ddf.ecostruxureit.com/ddfsearchapi/ddfSearch?search=*snmp*&size=9999&startingIndex=0"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    with open('ddf_files/ddf_manifest_download.json', 'wb') as download_file:
        download_file.write(response.content)
        download_file.close()
    return response.text

def download_ddf(ddf_id, ddf_filename, ddf_state):
    """Downloads the DDF file."""
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
    get_ddf_list()
    ddf_list = json.loads(get_ddf_list())
    for ddf in ddf_list:
        ddf_id = ddf['id']
        ddf_filename = ddf['fileName']
        ddf_state = ddf['ddfState']
        download_ddf(ddf_id, ddf_filename, ddf_state)
    os.chdir('ddf_files')
    os.rename('ddf_manifest_download.json','ddf_manifest.json')

def process_upgrade():
    """Upgrades DDF Files based on Version."""
    ddf_version_dictionary = {}
    with open('ddf_files/ddf_manifest.json') as existing_manifest:
        existing_ddf_manifest = json.load(existing_manifest)
        for existing_ddf in existing_ddf_manifest:
            ddf_version_dictionary[str(existing_ddf['fileName'])] = str(existing_ddf['ddfVersion'])
        ddf_list = json.loads(get_ddf_list())
        for ddf in ddf_list:
            ddf_id = ddf['id']
            ddf_filename = ddf['fileName']
            ddf_version = ddf['ddfVersion']
            ddf_state = ddf['ddfState']
            try:
                # Making attempt to check DDF version.
                if ddf_version_dictionary[str(ddf_filename)] != ddf_version:
                    download_ddf(ddf_id, ddf_filename, ddf_state)
            except:
                # Unable to check version. Adding/Upgrading DDF Anyway.
                download_ddf(ddf_id, ddf_filename, ddf_state)
        existing_manifest.close()
    os.remove('ddf_files/ddf_manifest.json')
    os.chdir('ddf_files')
    os.rename('ddf_manifest_download.json','ddf_manifest.json')

if __name__ == "__main__":
    if not os.path.exists('ddf_files'):
        os.makedirs('ddf_files')
    if os.path.exists('ddf_files/ddf_manifest.json'):
        process_upgrade()
    else:
        process_new()
