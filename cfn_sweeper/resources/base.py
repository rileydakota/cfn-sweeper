from abc import ABC, abstractmethod

class base_resource(ABC):
    """
    Abstract class for adding individual resource scanning support to cfn_sweeper
    All classes built from this require the resource_name property to be defined,
    and a gather() method to be implemented on the subclass.

    The resource_name property should be the cloudformation type of the resource
    (eg AWS::S3::Bucket).

    The gather() method should take a region property, and return a list of all physical
    resource ids for the resource type in question (for S3 Buckets - given the region of
    us-east-1, it would return a list of all the bucket names in us-east-1)
    """
    def resource_name(self):
        try:
            return self._resource_name
        except AttributeError:
            raise NotImplementedError('base_resources are required to have a resource name set')

    @abstractmethod
    def gather(self, region:str):
        pass