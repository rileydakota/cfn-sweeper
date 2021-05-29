from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):

    def __init__(self):
        self.resource_name = "AWS::Lambda::Function"

    def gather(self, region):
        results = []
        return results