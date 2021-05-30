from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):
    
    def __init__(self):
        self.resource_name = "AWS::DynamoDB::Table"


    def gather(self, region):
        result = []
        dynamodb = boto3.client('dynamodb',region_name=region)
        response = dynamodb.list_tables()
        for table in response['TableNames']:
            result.append(table)

        while 'LastEvaluatedTableName' in response:
            
            response = dynamodb.list_tables(ExclusiveStartTableName = response['LastEvaluatedTableName'])
            for i in response['TableNames']:
                result.append(i)
        else:   
            return result
 