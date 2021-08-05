from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):

    def __init__(self):
        self.resource_name = "AWS::KMS::Key"

    def gather(self, region):
        results = []
        kms = boto3.client('kms', region_name=region)
        paginator = kms.get_paginator('list_keys')
        for response in paginator.paginate():
            response_key_ids = [r.get('KeyId') for r in response['Keys']]
            results.extend(response_key_ids)
        return results