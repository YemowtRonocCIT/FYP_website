import requests
import json

HTTP_PREFIX = 'http://'

class ApiHandler(object):

    def __init__(self, api_ip_address=None):
        """
        Initializes the ApiHandler object. An API IP Address can be passed to 
        specify a remote IP address, or if left alone, will default to 
        127.0.0.1:5000

        api_ip_address (str[IP Address]): IP address of the API server
        """
        if api_ip_address is not None:
            self.base_url = "%s%s" % (HTTP_PREFIX, api_ip_address)
        else:
            self.base_url = "%s%s" % (HTTP_PREFIX, '127.0.0.1:5000')
        
        self.base_url += "%s"

    def get_data(self, url_suffix):
        """
        Sends GET request to API with given suffix

        url_suffix (str): Suffix to request specified data from API
        """
        url = self.base_url % (url_suffix)
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    def get_specific_data(self, url_suffix, identifier):
        """
        Sends GET request to API with given suffix and identifier for more
        specific request

        url_suffix (str): Suffix to request specified data from API
        identifier (str): Element to identify specific element (e.g. Sigfox ID)
        """
        extension = "%s%s" % (url_suffix, identifier)
        return self.get_data(extension)

    def remove_element(self, url_suffix, identifier):
        """
        Send DELETE request to API with the given suffix and identifier.
        This will delete the identified data from the database

        url_suffix (str): Suffix to delete specified data from API
        identifier (str): Identification of specific element (e.g. Sigfox ID)
        """
        url = self.base_url % (url_suffix, )
        url += "%s/" % (identifier, )
        response = requests.delete(url)
        return response.ok