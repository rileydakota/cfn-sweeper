import cfn_sweeper.resources.AWS_KMS_Key as kms
import pytest
import json
import boto3 # AWS SDK for Python
from moto import mock_kms


@mock_kms
def test_kms():

    kms_scanner_resource = kms.resource()

    scan_result = kms_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0

    kms_client = boto3.client('kms', region_name='us-east-1')
    kmscnt = 0
    while kmscnt < 10:
        kmscnt += 1
        kms_client.create_key()

    scan_result_us1 = kms_scanner_resource.gather('us-east-1')
    assert len(scan_result_us1) == 10


    scan_result_us2 = kms_scanner_resource.gather('us-east-2')
    assert len(scan_result_us2) == 0
    
    kms_client_other_region = boto3.client('kms', region_name='us-east-2')
    kmscnt = 0
    while kmscnt < 10:
        kmscnt += 1
        kms_client_other_region.create_key()
    
    scan_result_us1 = kms_scanner_resource.gather('us-east-1')
    scan_result_us2 = kms_scanner_resource.gather('us-east-2')
    assert len(scan_result_us1) == 10
    assert len(scan_result_us2) == 10 



