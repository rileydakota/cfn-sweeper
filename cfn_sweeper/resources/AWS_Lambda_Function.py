from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):

    def __init__(self):
        self.resource_name = "AWS::Lambda::Function"

    def gather(self, region):
        results = []
        client = boto3.client('lambda', region_name=region)
        function_paginator = client.get_paginator('list_functions')
        for response in function_paginator.paginate():
            response_function_names = [r.get('FunctionName') for r in response['Functions']]
            results.extend(response_function_names)
        return results