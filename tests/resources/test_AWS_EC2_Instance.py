import cfn_sweeper.resources.AWS_EC2_Instance as ec2
import pytest
import boto3
from moto import mock_ec2

@mock_ec2
def test_ec2_resource():
    ec2_scanner_resource = ec2.resource()
    
    scan_result = ec2_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0
    
    client = boto3.resource('ec2', region_name='us-east-1')
    client.create_instances(
    ImageId= 'aki-00806369',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
)

    
    assert ec2_scanner_resource.resource_name == 'AWS::EC2::Instance'
    
    scan_result = ec2_scanner_resource.gather(region='us-east-1')

    assert len(scan_result) == 1

    
    
