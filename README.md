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
