import boto3
from botocore.config import Config

cfn_config = Config(
    retries={
        'max_attempts': 10,
        'mode': 'adaptive'
    }
)


def load_cfn_resources(region: str) -> list:
    """
     Gets all the Cloudformation managed resources for the given AWS region

     Parameters:
         region (string): the AWS Region to scan

     Returns:
         An array of dict - containing the information of Cloudformation resources

    """
    cloudformation_client = boto3.client(
        service_name='cloudformation', region_name=region, config=cfn_config)
    stacks_in_account = []
    stack_paginator = cloudformation_client.get_paginator('list_stacks')

    stack_page_iterator = stack_paginator.paginate(
        StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
    for page in stack_page_iterator:
        stacks_in_account.extend(page['StackSummaries'])
    resource_paginator = cloudformation_client.get_paginator(
        'list_stack_resources')
    result = []
    for stack in stacks_in_account:
        resource_page_iterator = resource_paginator.paginate(
            StackName=stack['StackName'])
        for page in resource_page_iterator:
            for resource in page['StackResourceSummaries']:
                result.append(resource)
    return result


def get_all_cfn_resources_by_type(resource_array: list, resource_type: str) -> list:
    """
    Given a list of cloudformation stack resources, filters the resources by the specified type

    Parameters:
        resource_array (list): an Array of Cloudformation Stack Resources
        resource_type (string): the Name of the Cloudformation Resource type to filter for - example: AWS::EC2::Instance

    Returns:
        An array of dict - containing the filtered Cloudformation resources
    """
    result = []

    for resource in resource_array:
        if resource['ResourceType'] == resource_type:
            result.append(resource)
    return result


def is_managed_by_cloudformation(physical_resource_id: str, resource_array: list) -> bool:
    """
    Given a physical resource id and array of rources - returns if the resource is managed by cloudformation

    Parameters:
        physical_resource_id (string): The identifier of the resource - eg igw-09a7b4932e331edb2 or vpc-054a63a50efe678b3
        resource_array (list): an array of cloudformation stack resources

    Returns:
        boolean - if the resource is found in the list of resource_array
    """

    for resource in resource_array:
        if resource['PhysicalResourceId'] == physical_resource_id:
            return True
    else:
        return False
