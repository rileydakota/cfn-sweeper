import json
import yaml
from pprint import pprint
from cfn_sweeper.artwork import Artwork
class ScanReport():
    def __init__(self):
       self.__report_data = {}

    def add_resource_results(self, resource_type:str, managed_resources:list, unmanaged_resources:list):
        self.__report_data[resource_type] = {
            'managed': managed_resources,
            'unmanaged': unmanaged_resources
        }
    
    def print_to_yaml(self):    
        print(yaml.dump(self.__report_data))
    
    def print_to_json(self):
        print(json.dumps(self.__report_data))
        
    def print_to_pretty(self):
        Artwork.art()
        pprint(self.__report_data)


    def print_to_stdout(self):
        result = []

        for key in self.__report_data.keys():
            result.extend(self.__report_data[key]['unmanaged'])
            

        for unmanaged_item in result:
            print(unmanaged_item)
