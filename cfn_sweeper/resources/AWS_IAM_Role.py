from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):

    def __init__(self):
        self.resource_name = "AWS::IAM::Role"

    def gather(self, region):
        results = []
        iam = boto3.client('iam', region_name=region)
        role_paginator = iam.get_paginator('list_roles')
        for response in role_paginator.paginate():
            response_role_names = [r.get('RoleName') for r in response['Roles']]
            results.extend(response_role_names)
        return results
        
        
