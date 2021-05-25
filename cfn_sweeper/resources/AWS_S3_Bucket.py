from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):
    
    def __init__(self):
        self.resource_name = "AWS::S3::Bucket"

    def gather(self, region):
        results = []
        s3_client = boto3.client('s3', region_name=region)
        raw_response = s3_client.list_buckets()
        for bucket in raw_response['Buckets']:
            results.append(bucket['Name'])
        return results
