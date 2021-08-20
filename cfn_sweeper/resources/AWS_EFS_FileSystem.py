from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):
    
    def __init__(self):
        self.resource_name = "AWS::EFS::FileSystem"

    def gather(self, region: str):
        results = []
        efs = boto3.client('efs',  region_name=region)
        fs_paginator = efs.get_paginator('describe_file_systems')
        for response in fs_paginator.paginate():
            response_fs_names = [r.get('FileSystemId') for r in response['FileSystems']]
            results.extend(response_fs_names)
        return results