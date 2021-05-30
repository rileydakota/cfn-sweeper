from cfn_sweeper.resources.base import base_resource
import boto3

class resource(base_resource):
    
    def __init__(self):
        self.resource_name = "AWS::EC2::Instance"

#Can return the below as well if needed: ,    "Platform:": instance.platform,   "Type:": instance.instance_type,   "PublicIPv4:": instance.public_ip_address, "AMI:": #instance.image.id, "State:": instance.state
    def gather(self, region):
        result = []
        ec2 = boto3.resource('ec2',region_name=region)
        for instance in ec2.instances.all():
            result.append(instance.id)
        return result
