import cfn_sweeper.resources.AWS_EFS_FileSystem as efs
import pytest
import boto3
from moto import mock_efs

@mock_efs
def test_efs_resource():

    efs_fs_scanner_resource = efs.resource()

    assert efs_fs_scanner_resource.resource_name == 'AWS::EFS::FileSystem'

    scan_result = efs_fs_scanner_resource.gather('us-east-1')
    assert len(scan_result) == 0
    
    client = boto3.client('efs', region_name='us-east-1')
    client.create_file_system()

    assert len(efs_fs_scanner_resource.gather(region='us-east-1')) == 1
    assert len(efs_fs_scanner_resource.gather(region='us-east-2')) == 0

    for x in range(0,100):
        client.create_file_system()

    assert len(efs_fs_scanner_resource.gather(region='us-east-1')) == 101
