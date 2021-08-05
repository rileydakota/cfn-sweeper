# cfn-sweeper - find all the unmanaged resources in your account!
A CLI Tool to find resources in an AWS Account not actively managed by Cloudformation!

Wanting to understand how many resources in your AWS Account are managed by Cloudformation? This is the tool for you!

## Installation

Download the package from PyPI:
```pip install cfn-sweeper```

Or install directly from source:
```git clone git@github.com:rileydakota/cfn-sweeper.git && python3 cfn-sweeper/setup.py```

## Usage

```bash
cfn-sweeper ---output pretty --region us-east-1

 ______  ______ __   __                                      
/\  ___\/\  ___/\ "-.\ \                                     
\ \ \___\ \  __\ \ \-.  \                                    
 \ \_____\ \_\  \ \_\\"\_\                                   
 __________/_/  __/_______  ______  ______ ______  ______    
/\  ___\/\ \  _ \ \/\  ___\/\  ___\/\  == /\  ___\/\  == \   
\ \___  \ \ \/ ".\ \ \  __\\ \  __\\ \  _-\ \  __\\ \  __<   
 \/\_____\ \__/".~\_\ \_____\ \_____\ \_\  \ \_____\ \_\ \_\ 
  \/_____/\/_/   \/_/\/_____/\/_____/\/_/   \/_____/\/_/ /_/ 
  
  The umanaged resource detector tool!
  -----------------------------------------------------------
                        Run Report
  -----------------------------------------------------------
  1236 resources found created by Cloudformation!
  34 resources not managed by Cloudformation!
  2 Cloudformation managed resources not found!
  4 resources not verifed (not yet supported)!
  
  Unmanaged Resources:
    AWS::IAM::Role
      1243-myrolecreatedinconsole
      hand-createdrole
    AWS::EC2::Instance
      i-23054dfi514fdewqi2541
      i-239mvfewnmiwemf273492
   ...
   ...
```
### Available arguments

`--output`

Controls the output format of the results. Printed to stdout.
Valid values: `pretty`, `json`, `yaml`

`--region`

The AWS Region from which we will run `describe-stacks` and look for the various resources in
Valid values: any valid AWS region in kebab case format (eg `us-east-1`)

`--filter-types`

Allows you to exclude particular AWS Resource types based on the Cloudformation type (eg `AWS::IAM::Role` or `AWS::EC2::Instance`) 
Valid values: any Cloudformation resource type that is supported by the tool today (see https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html for reference). Multiple values can be supplied


`--filter-tag-keys`

Allows you to exclude particular AWS Resources based on the presence of a particular tag key on the resource. This will only be applied to AWS Resources that support tagging.
Valid values: any string that is a valid tag - multiple values can be supplied

### Supported Cloudformation Types

`AWS::IAM::Role`

`AWS::EC2::Instance`

`AWS::Lambda::Function`

`AWS::S3::Bucket`

`AWS::KMS::Key`

### Using as a Python Module

```python
import cfn_sweeper

cfn_managed_resources = cfn_sweeper.get_managed_resources()
unmanaged_resources = cfn_sweeper.get_unmanaged_resources(cfn_managed_resources)

```
