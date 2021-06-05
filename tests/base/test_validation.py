import argparse
from cfn_sweeper.validation import ValidateRegion,Validateoutput,Validatefilter
import pytest 
from contextlib import contextmanager


@contextmanager
def not_raises(exception):
        try:
            yield
        except exception:
            raise pytest.fail("DID RAISE {0}".format(exception))


def test_required_unknown():
    """ Try to perform sweep on something that isn't an option. """
    parser=argparse.ArgumentParser()
    parser.add_argument('--region',
                        help='Enter a region like us-east-2.',
                        dest="region",
                        action=ValidateRegion,
                        required=True)
    parser.add_argument('--output',
                        help='pretty, json, yaml',
                        dest="output",
                        action=Validateoutput,
                        nargs="?",
                        default="yaml"
                        )
    parser.add_argument('--filter-types',
                        help='eg: AWS::IAM::Role or AWS::EC2::Instance. Using  "ALL"  with no quotes and we will run it for all current supported resource types',
                        nargs='+',
                        dest="types",
                        action=Validatefilter,
                        required=True)
    parser.add_argument('--tag_keys',
                        help='Allows you to exclude particular AWS Resources based on the presence of a particular tag key on the resource. This will only be applied to AWS Resources that support tagging. Valid values: any string that is a valid tag - multiple values can be supplied.',
                        dest="tags")
    
    #This should raise an error since this will cause a SystemExit since bad params were passed in 
    args = ["--region", "NADA",'--output', "NADA",'--filter-types',"NADA"]
    with pytest.raises(SystemExit):
        parser.parse_args(args)
        
        
        
        
    #This should NOT raise an error since good params were passed into the parser
    args = ["--region", "us-east-1",'--output', "yaml",'--filter-types',"AWS::EC2::Instance"]    
    with not_raises(SystemExit):
        parser.parse_args(args)