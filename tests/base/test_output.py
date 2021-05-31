from cfn_sweeper.base.output import ScanReport
import pytest

def test_ScanReport(capsys):

    report = ScanReport()
    report.add_resource_results(resource_type='AWS::S3::Bucket', managed_resources=['mycfnmadebucket'], unmanaged_resources=['mynoncfnbucket'])

    assert report._ScanReport__report_data == {
        'AWS::S3::Bucket':{
            'managed':['mycfnmadebucket'],
            'unmanaged':['mynoncfnbucket']
        }
    }

    report.print_to_json()
    captured = capsys.readouterr()
    assert captured.out == '{"AWS::S3::Bucket": {"managed": ["mycfnmadebucket"], "unmanaged": ["mynoncfnbucket"]}}\n'
    
    report.print_to_yaml()
    captured = capsys.readouterr()
    assert captured.out == 'AWS::S3::Bucket:\n  managed:\n  - mycfnmadebucket\n  unmanaged:\n  - mynoncfnbucket\n\n'

    report.print_to_stdout()
    captured = capsys.readouterr()
    assert captured.out == 'mynoncfnbucket\n'