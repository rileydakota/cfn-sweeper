import argparse
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--region',
                        help='Enter a region like us-east-2.',
                        dest="region")
    parser.add_argument('--output',
                        help='pretty, json, yaml',
                        dest="output")
    parser.add_argument('--filter-types',
                        help='eg: AWS::IAM::Role or AWS::EC2::Instance.',
                        dest="types")
    parser.add_argument('--tag_keys',
                        help='Allows you to exclude particular AWS Resources based on the presence of a particular tag key on the resource. This will only be applied to AWS Resources that support tagging. Valid values: any string that is a valid tag - multiple values can be supplied.',
                        dest="tags")

    args = parser.parse_args()

    output = args.output
    
    print("The region supplied was:" + " " + str(args.region) + ", " + "the output supplied was:" + " " + str(args.output) + ", " + "the types supplied was:" + " " + str(args.types) + ", " + "the tags supplied was:" + " " + str(args.tags) +
          ", " + "and here is the snek if found" + '\n')

    if args.output:
        f = open(output, "a")
        f.write(str(result))


if __name__ == '__main__':
    main()
