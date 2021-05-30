# test_AWS_IAM_Role.py
import cfn_sweeper.resources.AWS_IAM_Role as iam
import pytest
import json
import boto3 # AWS SDK for Python
from moto import mock_iam # since we're going to mock DynamoDB service

@mock_iam
def test_iam():
    
    iam_scanner_resource = iam.resource()
    
    
    scan_result = iam_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0    
    
    """
    Create and mock role creation and trust relation
    """
    
    assume_role_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "support.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })
    
    
    roles = boto3.client('iam', region_name='us-east-1')
    rolecnt = 0
    while rolecnt < 10:
        rolecnt += 1
        roles.create_role(
            RoleName='RoleName' + str(rolecnt),
            AssumeRolePolicyDocument = assume_role_policy_document,
            Description='RoleName' + str(rolecnt),
            Tags=[
                {
                    'Key': 'mock_role',
                    'Value': 'mock_role' + str(rolecnt)
                },
            ]
        )
        

    """
    Test if our mock role(s) are ready and we can return it
    """
    
    assert iam_scanner_resource.resource_name == 'AWS::IAM::Role'
    
    
    scan_result = iam_scanner_resource.gather(region='us-east-1')

    assert len(scan_result) == rolecnt

    assert  any("RoleName" in s for s in scan_result)
    




