from importlib import import_module 
import os

def get_aws_modules(files:list) -> list:
    return filter(lambda x: x.startswith('AWS'), files)

def get_module_dir() -> str:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir_len = len(root_dir)
    return root_dir[:root_dir_len - 4] + 'resources'


class PluginManager:
    def __init__(self):
        self.modules = {}
        module_dir_files = os.listdir(get_module_dir())
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