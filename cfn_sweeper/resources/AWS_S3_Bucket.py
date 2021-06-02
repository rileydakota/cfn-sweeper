from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):
    
    def __init__(self):
        self.resource_name = "AWS::S3::Bucket"

    def gather(self, region):
        results = []
        s3_client = boto3.client('s3', region_name=None)
        raw_response = s3_client.list_buckets()
        for bucket in raw_response['Buckets']:
            bucket_region = s3_client.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint']
            if region == 'us-east-1':
                if bucket_region == None:
                   results.append(bucket['Name']) 
            elif bucket_region == region:
                results.append(bucket['Name'])
           

        return results
