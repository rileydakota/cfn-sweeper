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
cfn-sweeper --region us-east-1 --filter-types AWS::S3::Bucket AWS::EC2::Instance AWS::EFS::FileSystem
AWS::EC2::Instance:
  managed:
  - i-04738a0664ab77af4
  unmanaged: []
AWS::S3::Bucket
  managed: []
  unmanaged:
  - my-leftover-bucket
AWS::EFS::FileSystem
  managed:
  - fs-123456
  unmanaged:
  - fs-789101
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


`--filter-tag-keys` [WIP]

Allows you to exclude particular AWS Resources based on the presence of a particular tag key on the resource. This will only be applied to AWS Resources that support tagging.
Valid values: any string that is a valid tag - multiple values can be supplied

### Supported Cloudformation Types

`AWS::IAM::Role` - (Global resoures are experimental at this time, use with caution)

`AWS::EC2::Instance`

`AWS::Lambda::Function`

`AWS::S3::Bucket`

`AWS::KMS::Key`

`AWS::EFS::FileSystem`

### Using as a Python Module

TBD

### FAQ

TBD
