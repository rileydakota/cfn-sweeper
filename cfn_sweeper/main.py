import argparse
from cfn_sweeper.base.cfn_resources import load_cfn_resources, get_all_cfn_resources_by_type, is_managed_by_cloudformation
from cfn_sweeper.base.runner import PluginManager
from cfn_sweeper.base.output import ScanReport
from cfn_sweeper.validation import ValidateRegion,Validateoutput,Validatefilter

    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--region',
                        help='Enter a region like us-east-2.',
                        dest="region",
                        action=ValidateRegion,
                        required=True)
    parser.add_argument('--output',
                        help='pretty, json, yaml, stdout',
                        dest="output",
                        action=Validateoutput,
                        nargs="?",
                        default="yaml"
                        )
    parser.add_argument('--filter-types',
                        help='eg: AWS::IAM::Role or AWS::EC2::Instance.',
                        nargs='+',
                        dest="types",
                        action=Validatefilter,
                        required=True)
    parser.add_argument('--tag_keys',
                        help='Allows you to exclude particular AWS Resources based on the presence of a particular tag key on the resource. This will only be applied to AWS Resources that support tagging. Valid values: any string that is a valid tag - multiple values can be supplied.',
                        dest="tags")

    #TODO: add argument validation - including regex for patterns
    args = parser.parse_args()

    #TODO: inital shot at this - refactor later
    region = args.region
    types = args.types
    output = args.output
    cfn_resources = load_cfn_resources(region)
    runner = PluginManager()
    
    #TODO: abstract result into its own class - so we can easily output to different formats
    report = ScanReport() 
    for resource_type in types:
        resources_in_cloudformation = get_all_cfn_resources_by_type(cfn_resources, resource_type)
        try:
            resources_in_account = runner.gather_resource(region=region, resource_name=resource_type)
        except NotImplementedError:
            print('Sorry - {} isn''t supported just yet!'.format(
                resource_type
            ))
            continue

        managed_resources = []
        unmanaged_resources = []
        for resource in resources_in_account:
            cfn_managed = is_managed_by_cloudformation(physical_resource_id=resource, resource_array=resources_in_cloudformation)
            if cfn_managed:
              managed_resources.append(resource)
            else:
              unmanaged_resources.append(resource)
        report.add_resource_results(resource_type=resource_type, managed_resources=managed_resources, unmanaged_resources=unmanaged_resources)
    
    
    if output == 'yaml':
      report.print_to_yaml()
    elif output == 'json':
      report.print_to_json()
    elif output == 'stdout':
      report.print_to_stdout()
    elif output == 'pretty':
      report.print_to_pretty()
    










    

    


if __name__ == '__main__':
    main()
