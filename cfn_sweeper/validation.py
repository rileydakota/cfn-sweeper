import sys
import re
import argparse

class ValidateRegion(argparse.Action):
    """Validate Region"""
    def __call__(self, parser, namespace, values, option_string=None):
        regex = re.compile('(us(-gov)?|ap|ca|cn|eu|sa)-(central|(north|south)?(east|west)?)-\d', re.I)
        match = regex.match(str(values))
        if bool(match) == False:
            sys.exit("--region parameter must be listed in the code portion of this table: https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints")
        else:
            setattr(namespace, self.dest, values)

class Validateoutput(argparse.Action):
    """Validate Output"""        
    def __call__(self, parser, namespace, values, option_string=None):
        output = ['pretty', 'json', 'yaml','stdout']
        if not values in output:
            sys.exit("--output parameter currently only supports: " + str(output))
        else:
            setattr(namespace, self.dest, values)

class Validatefilter(argparse.Action):
    """Validate Filter Types"""
    def __call__(self, parser, namespace, values, option_string=None):
        regex = re.compile('AWS::[0-z]*::[0-z]*', re.I)
        for value in values:
           match = regex.match(str(value))
        if match:
            setattr(namespace, self.dest, values)
        else:
            sys.exit("--filter-types parameter not valid, please look at the README and check: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html ")
