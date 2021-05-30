# test_AWS_DynamoDB_Table.py
import cfn_sweeper.resources.AWS_DynamoDB_Table as dynamo
import pytest
import boto3 # AWS SDK for Python
from moto import mock_dynamodb2 # since we're going to mock DynamoDB service

@mock_dynamodb2
def test_dynamo_db():
    
    dynamo_scanner_resource = dynamo.resource()
    
    
    scan_result = dynamo_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0    
    
    """
    Create database resource and mock table
    """
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    dbcnt = 0
    while dbcnt < 105:
        dbcnt += 1
        dynamodb.create_table(TableName="TableName" + str(dbcnt),
                                  KeySchema=[
                                      {
                                            'AttributeName': 'Test',
                                            'KeyType': 'HASH'
                                      }
                                  ],
                                  AttributeDefinitions=[
                                      {
                                          'AttributeName': 'Test',
                                          'AttributeType': 'N'
                                      }
                                  ],
                                  ProvisionedThroughput={
                                      'ReadCapacityUnits': 1,
                                      'WriteCapacityUnits': 1
                                  }
                                  )
        

    """
    Test if our mock table is ready and we can return it
    """
    
    assert dynamo_scanner_resource.resource_name == 'AWS::DynamoDB::Table'
    
    
    scan_result = dynamo_scanner_resource.gather(region='us-east-1')


    assert len(scan_result) == dbcnt




