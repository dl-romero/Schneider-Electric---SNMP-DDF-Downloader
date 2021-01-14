
import requests

def get_ddf_list():
    """Gets the SNMP DDF List in JSON from SE."""
    url = "https://ddf.ecostruxureit.com/ddfsearchapi/ddfSearch?search=*snmp*&size=9999&startingIndex=0"
    payload={}
    headers = {
    'Cookie': '__cfduid=d6407104b8a441a603ac1bb0dd53cc5931610650522'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

if __name__ == "__main__":
    print(get_ddf_list())
