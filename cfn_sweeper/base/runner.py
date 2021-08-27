from importlib import import_module
from pkgutil import walk_packages
import os

def get_aws_modules(files:list) -> list:
    '''
    Given a list of files, returns a list of the files that are
    prefixed with the AWS_ prefix

    This is used to filter out files that are required in the directory,
    such as __init__py or the abstract class 

    Parameters:
        files (list): an Array of strings - file names
    '''

    return list(filter(lambda x: x.startswith('AWS_'), files))

def get_module_dir() -> str:
    '''
    Returns the absolute directory of the resources folder - where the modules
    for AWS resources are located
    '''
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir_len = len(root_dir)
    return root_dir[:root_dir_len - 4] + 'resources'

def get_package_modules(package_path:str) -> list:
    result = []
    for package in walk_packages([package_path]):
        result.append(package.name)

    return result


class PluginManager:
    '''
    This class is used to manage and interact with the various AWS resource modules
    stored in the cfn_sweeper/resources section of the project. Upon initialization -
    the PluginManager class will dynamically load each module, and load it into a
    dict object with a key of the resource_name (eg - AWS::S3::Bucket or 
    AWS::EC2::Instance), and the modules corresponding gather() function as the value. 
    The dict shouldn't be directly interacted with - instead this class exposes a 
    gather_resource() method that expects a cloudformation resource_name, and aws region.
    The method will then look for a matching key in the dict - and execute its associated
    gather() method with the provided region parameter.
    '''
    
    def __init__(self):
        self.modules = {}
        module_dir_files = get_package_modules(get_module_dir())
        aws_modules = get_aws_modules(module_dir_files)
        for module in aws_modules:
            
            module_path = 'cfn_sweeper.resources.{}'.format(module.split('.')[0])
            try:
                loaded_module = import_module(module_path)
                resource = loaded_module.resource()
                self.modules[resource.resource_name] = resource.gather

            except ModuleNotFoundError as e:
                print(e)
                print('unable to load {}'.format(module))

    def gather_resource(self, region:str, resource_name:str):
        try:
            result = self.modules[resource_name](region=region)
            return result
        except KeyError as e:
            print(e)
            raise NotImplementedError