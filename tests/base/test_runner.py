from cfn_sweeper.base.runner import PluginManager, get_aws_modules, get_module_dir, get_package_modules
import uuid
import pytest

def test_get_aws_modules():
    list_dir = [
        'AWS_EC2_Instance.py',
        'AWS_IAM_Role.py',
        'NOT_AN_AWS_MODULE',
        '__init__.py',
        'base.py'
    ]

    result = get_aws_modules(list_dir)
    assert '__init__.py' not in result
    assert 'base.py' not in result
    assert 'NOT_AN_AWS_MODULE' not in result
    assert len(result) == 2
    assert 'AWS_EC2_Instance.py' in result
    assert 'AWS_IAM_Role.py' in result

def test_get_module_dir(mocker):
    mocker.patch(
        'cfn_sweeper.base.runner.os.path.dirname',
        return_value='/home/randomuser/cfn-sweeper/cfn-sweeper/base'
    )
    
    plugin_dir = get_module_dir()
    assert plugin_dir == '/home/randomuser/cfn-sweeper/cfn-sweeper/resources'

def test_get_package_modules(mocker):
    mocker.patch(
        'cfn_sweeper.base.runner.walk_packages',
        return_value=[
            FakePkgUtilModuleClass(name='module1'),
            FakePkgUtilModuleClass(name='module2')    
        ]
    )

    result = get_package_modules('module_path')
    assert len(result) == 2
    assert 'module1' in result
    assert 'module2' in result

def test_PluginManager(mocker):
    mocker.patch(
        'cfn_sweeper.base.runner.get_package_modules',
        return_value=[
            'AWS_EC2_Instance.py',
            'AWS_S3_Bucket.py',
            '__init__.py',
            'NOT_AN_AWS_MODULE.py'
        ]
    )

    mocker.patch(
        'cfn_sweeper.base.runner.os.path.dirname',
        return_value='/home/randomuser/cfn-sweeper/cfn-sweeper/base'
    )
 
    mocker.patch(
        'cfn_sweeper.base.runner.import_module',
        return_value=FakeModuleClass()
    )

    runner = PluginManager()
    assert runner.gather_resource(region='us-east-1', resource_name='AWS::Resource::Thing') == [
        'aws-thing-1',
        'aws-thing-2'
    ]

    with pytest.raises(NotImplementedError) as error_info:
        runner.gather_resource(region='us-east-1', resource_name='AWS::S3::Bucket')
    assert "NotImplementedError" in str(error_info)

""" Sadly not sure of a better way to test this - but essentually creating fake classes to simulate
    how our plugins would behave when dynamically imported using import_lib
"""

class FakeModuleClass():
    def resource(self):
        return FakeResourceClass()

class FakeResourceClass():
    def __init__(self):
        self.resource_name = 'AWS::Resource::Thing'

    def gather(self, region):
        return [
            'aws-thing-1',
            'aws-thing-2'
        ]

class FakePkgUtilModuleClass():
    def __init__(self, name):
        self.name = name