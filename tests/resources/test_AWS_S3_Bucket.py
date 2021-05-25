import cfn_sweeper.resources.AWS_S3_Bucket as bucket
import pytest
import boto3
from moto import mock_s3

@mock_s3
def test_s3_resource():
    s3_scanner_resource = bucket.resource()
    
    scan_result = s3_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0
    
    client = boto3.client('s3', region_name='us-east-1')
    client.create_bucket(Bucket='bucket1')
    client.create_bucket(Bucket='bucket2')

    print(bucket)
    
    assert s3_scanner_resource.resource_name == 'AWS::S3::Bucket'
    
    scan_result = s3_scanner_resource.gather(region='us-east-1')
    assert len(scan_result) == 2
    assert 'bucket1' in scan_result
    assert 'bucket2' in scan_result