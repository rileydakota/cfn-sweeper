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
  
    assert s3_scanner_resource.resource_name == 'AWS::S3::Bucket'
    
    scan_result = s3_scanner_resource.gather(region='us-east-1')
    assert len(scan_result) == 2
    assert 'bucket1' in scan_result
    assert 'bucket2' in scan_result

    client.delete_bucket(Bucket='bucket1')
    client.delete_bucket(Bucket='bucket2')
    
    # test pagination
    for num in range(500):
        client.create_bucket(Bucket='bucket{}'.format(
            num
        ))
    scan_result = s3_scanner_resource.gather(region='us-east-1')
    assert len(scan_result) == 500

@mock_s3
def test_s3_resource_multi_region():

    s3_scanner_resource = bucket.resource()
    
    scan_result = s3_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0

    client = boto3.client('s3', region_name='us-east-1')

    east_bucket_name='us-east-1-bucket'
    west_bucket_name='us-west-1-bucket'
    client.create_bucket(Bucket=east_bucket_name)
    client.create_bucket(Bucket=west_bucket_name, CreateBucketConfiguration={'LocationConstraint':'us-west-1'})

    us_east_1_scan_result = s3_scanner_resource.gather(region='us-east-1')
    us_west_1_scan_result = s3_scanner_resource.gather(region='us-west-1')

    assert len(us_east_1_scan_result) == 1
    assert len(us_west_1_scan_result) == 1
    assert east_bucket_name not in us_west_1_scan_result
    assert west_bucket_name not in us_east_1_scan_result