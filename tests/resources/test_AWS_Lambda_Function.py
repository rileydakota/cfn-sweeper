from cfn_sweeper import resources
from cfn_sweeper.resources import AWS_Lambda_Function as aws_lambda
import zipfile
import io
import pytest
import boto3
from botocore.exceptions import ClientError
from moto import mock_lambda, mock_iam


@mock_lambda
def test_lambda_resoure():
    lambda_scanner_resource = aws_lambda.resource()

    assert len(lambda_scanner_resource.gather('us-east-1')) == 0

    client = boto3.client('lambda', region_name='us-east-1')
    client.create_function(
        FunctionName="testFunction",
        Role=get_role_name(),
        Code ={"ZipFile": get_test_zip_file1()},
        Handler="lambda_function.lambda_handler",
        Runtime='python2.7'
    )

    assert len(lambda_scanner_resource.gather('us-east-1')) == 1
    assert len(lambda_scanner_resource.gather('us-east-2')) == 0

    for x in range(0,500):
        client.create_function(
            FunctionName='MyTestFunction{}'.format(str(x)),
            Role=get_role_name(),
            Code ={"ZipFile": get_test_zip_file1()},
            Handler="lambda_function.lambda_handler",
            Runtime='python2.7'
        )

    assert len(lambda_scanner_resource.gather('us-east-1')) == 501
    assert len(lambda_scanner_resource.gather('us-east-2')) == 0



def get_role_name():
    with mock_iam():
        iam = boto3.client("iam")
        try:
            return iam.get_role(RoleName="my-role")["Role"]["Arn"]
        except ClientError:
            return iam.create_role(
                RoleName="my-role",
                AssumeRolePolicyDocument="some policy",
                Path="/my-path/",
            )["Role"]["Arn"]


def _process_lambda(func_str):
    zip_output = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED)
    zip_file.writestr("lambda_function.py", func_str)
    zip_file.close()
    zip_output.seek(0)
    return zip_output.read()


def get_test_zip_file1():
    pfunc = """
def lambda_handler(event, context):
    print("custom log event")
    return event
"""
    return _process_lambda(pfunc)
