import argparse
from pprint import pprint
from cfn_sweeper.base.cfn_resources import load_cfn_resources, get_all_cfn_resources_by_type, is_managed_by_cloudformation
from cfn_sweeper.base.runner import PluginManager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--region',
                        help='Enter a region like us-east-2.',
                        dest="region",
                        required=True)
    parser.add_argument('--output',
                        help='pretty, json, yaml',
                        dest="output")
    parser.add_argument('--filter-types',
                        help='eg: AWS::IAM::Role or AWS::EC2::Instance.',
                        nargs='+',
                        dest="types",
                        required=True)
    parser.add_argument('--tag_keys',
                        help='Allows you to exclude particular AWS Resources based on the presence of a particular tag key on the resource. This will only be applied to AWS Resources that support tagging. Valid values: any string that is a valid tag - multiple values can be supplied.',
                        dest="tags")

    #TODO: add argument validation - including regex for patterns
    args = parser.parse_args()

    #TODO: inital shot at this - refactor later
    region = args.region
    types = args.types
    cfn_resources = load_cfn_resources(region)
    runner = PluginManager()
    
    #TODO: abstract result into its own class - so we can easily output to different formats
    result = {}
    for resource_type in types:
        result[resource_type] = {
            'managed':[],
            'unmanaged':[]
        }
        resources_in_cloudformation = get_all_cfn_resources_by_type(cfn_resources, resource_type)
        try:
            resources_in_account = runner.gather_resource(region=region, resource_name=resource_type)
        except NotImplementedError:
            print('Sorry - {} isn''t supported just yet!'.format(
                resource_type
            ))
        for resource in resources_in_account:
            cfn_managed = is_managed_by_cloudformation(physical_resource_id=resource, resource_array=resources_in_cloudformation)
            if cfn_managed:
                result[resource_type]['managed'].append(resource)
            else:
                result[resource_type]['unmanaged'].append(resource)
    print(result)










    

    


if __name__ == '__main__':
    main()
