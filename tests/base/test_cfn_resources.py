from cfn_sweeper.base.cfn_resources import is_managed_by_cloudformation, get_all_cfn_resources_by_type, load_cfn_resources
import pytest
import boto3
import json
from moto import mock_cloudformation

@mock_cloudformation
def test_load_cfn_resources():
    
    dummy_template1 = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Stack 3",
    "Resources": {
        "VPC": {"Properties": {"CidrBlock": "192.168.0.0/16"}, "Type": "AWS::EC2::VPC"}
    },
    }

    dummy_template2 = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Stack 1",
    "Resources": {
        "EC2Instance1": {
            "Type": "AWS::EC2::Instance",
            "Properties": {
                "ImageId": '11111111122334324',
                "KeyName": "dummy",
                "InstanceType": "t2.micro",
                "Tags": [
                    {"Key": "Description", "Value": "Test tag"},
                    {"Key": "Name", "Value": "Name tag for tests"},
                ],
            },
        }
    },
}
    
    client = boto3.client('cloudformation', 'us-east-1')
    client.create_stack(StackName="test_stack1", TemplateBody=json.dumps(dummy_template1))
    client.create_stack(StackName="test_stack2", TemplateBody=json.dumps(dummy_template2))

    cfn_resources = load_cfn_resources('us-east-1')

    assert len(cfn_resources) == 2
    assert cfn_resources[0]['PhysicalResourceId'] 
    assert cfn_resources[0]['ResourceType']
    assert cfn_resources[0]['ResourceStatus']
    
    client.delete_stack(StackName="test_stack1")
    client.delete_stack(StackName="test_stack2")

    cfn_resources = load_cfn_resources('us-east-1')
    assert len(cfn_resources) == 0

def test_get_all_cfn_resources_by_type():
    resource_array = [{
        "ResourceType":"AWS::EC2::Instance"
    },{
        "ResourceType":"AWS::Lambda::Function"
    },
    {
        "ResourceType":"AWS::IAM::Role"
    }]

    result = get_all_cfn_resources_by_type(resource_array, 'AWS::EC2::Instance')

    assert type(result) is list
    assert len(result) == 1
    assert result[0]['ResourceType'] == 'AWS::EC2::Instance'

    resource_array = [{
        "ResourceType":"AWS::Lambda::Function"
    },{
        "ResourceType":"AWS::Lambda::Function"
    },
    {
        "ResourceType":"AWS::IAM::Role"
    }]

    result = get_all_cfn_resources_by_type(resource_array, 'AWS::Lambda::Function')

    assert len(result) == 2
    assert result[0]['ResourceType'] == 'AWS::Lambda::Function'
    assert result[1]['ResourceType'] == 'AWS::Lambda::Function'

    result = get_all_cfn_resources_by_type(resource_array, 'AWS::EC2::VPC')

    assert len(result) == 0

def test_is_managed_by_cloudformation():
    resource_array = [{
        "PhysicalResourceId":"vpc-1234"
    },{
        "PhysicalResourceId":"vpc-5678"
    },{
        "PhysicalResourceId":"vpc-7891"
    }]


    assert is_managed_by_cloudformation("vpc-1234", resource_array) == True
    assert is_managed_by_cloudformation("vpc-7891", resource_array) == True
    assert is_managed_by_cloudformation("vpc-1112", resource_array) == False