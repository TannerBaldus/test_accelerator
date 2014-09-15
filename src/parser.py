from parse_tools import print_test_names
from argparse import  ArgumentParser
from settings import  INSTALLED_FRAMEWORKS
import os

parser = ArgumentParser()

parser.add_argument("--framework", dest="framework", required=True,
                    help="Which framework to parse.")


parser.add_argument("--files", "-f", action="store", dest="files", default=os.getcwd(),
                    help="A directory or comma separated list of files to search")

parser.add_argument("--pattern", "-p", action="store", dest="pattern",
                    help="glob pattern for files to search", default='*')

parser.add_argument("--recursive", "-r", action="store_true", dest="recursive",
                        help="Whether to recursively search directory", default=False)

parser.add_argument("--agent", "-a", action="store", required=True, dest="agents", type=int,
                    help="How many agents are you using")



def get_framework(arguments):
    framework = INSTALLED_FRAMEWORKS.get(arguments.framework)
    if not framework:
        raise Exception('{} not in  INSTALLED_FRAMEWORKS check settings.py'.format(framework))
    return framework


def get_nodes(arguments):
    framework = get_framework(arguments)
    nodes = framework.get('nodes')
    if not nodes:
        raise Exception("Nodes not defined in settings for {}".format(framework))
    return nodes


def get_strip(arguments):
    framework = get_framework(arguments)
    strip = framework.get('strip')
    if not framework:
        raise Exception('Strip variable not set in {}'.format(framework))
    return strip


def testfile_parse(arguments):
    nodes = get_nodes(arguments)
    strip = get_strip(arguments)
    print_test_names(arguments.agents, arguments.files, arguments.recursive, arguments.pattern, nodes, strip)


def main():
    arguments = parser.parse_args()
    testfile_parse(arguments)

if __name__ == '__main__':
    main()
