from cfn_sweeper.base.runner import PluginManager, get_aws_modules, get_module_dir
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
    
