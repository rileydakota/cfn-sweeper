import argparse

ascii_snek_big = """\
    --..,_                     _,.--.
       `'.'.                .'`__ o  `;__. 
          '.'.            .'.'`  '---'`  `
            '.`'--....--'`.'
              `'--....--'`
"""

ascii_snek_smoll = """\
    --..,_               _,.--.
       `'.'.           .'`__ o  `;__. 
          '.'.       .'.'`  '---'`  `
            '.`'..--'`
              `'--....--'`
"""


def snek(n):
    if n == 'smoll':
        a = ascii_snek_smoll
    elif n == 'big':
        a = ascii_snek_big
    else:
        a = "No snek could be found for your argument"
    return a


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Enter a name like smoll or big")
    parser.add_argument('--outputDirectory',
                        help='Path to the output that contains the resumes.',
                        dest="output")

    args = parser.parse_args()

    result = snek(args.name)
    output = args.output + 'snek.txt'

    print("The name supplied was:" + " " + str(args.name) +
          " " + "and here is the snek if found" + '\n')
    print(result)

    if args.output:
        f = open(output, "a")
        f.write(str(result))


if __name__ == '__main__':
    main()
