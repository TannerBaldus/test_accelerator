__author__ = 'tanner'
from settings import INSTALLED_FRAMEWORKS
import argparse
import os.path

parser = argparse.ArgumentParser()
def check_negative(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


parser.add_argument("--framework", dest="framework", required=True,
                    help="Which framework to parse.")

parser.add_argument("--testrunner", dest="test_runner",required=True,
                    help="Path to the testrunner")

parser.add_argument("--files", "-f", action="store", dest="files", required=True,
                    help="A directory or comma separated list of files to search")

parser.add_argument("--pattern", "-p", action="store", dest="pattern",
                    help="glob pattern for files to search", default='*')

parser.add_argument("--recursive", "-r", action="store_true", dest="recursive",
                        help="Whether to recursively search directory", default=False)

parser.add_argument("--test_target", "-t", action="store", dest="test_target", required=True,
                     help='The compiled test file. ex. tests.dll')

parser.add_argument("--makefile" "-m", action="store", dest="makefile_path",
                  help="Path to write makefile to", default=os.path.join(os.getcwd(), 'Makefile'))

parser.add_argument("--agent", "-a", action="store", required=True, dest="agents", type=check_negative,
                    default=1, help="How many agents are you using")


def get_framework(arguments):
    framework = INSTALLED_FRAMEWORKS.get(arguments.framework)
    if not framework:
        raise Exception('{} not in  INSTALLED_FRAMEWORKS check settings.py'.format(framework))
    return framework


def get_makefile(arguments):
    framework = get_framework(arguments)
    makefile = framework.get('makefile')
    if not makefile:
        raise Exception('No makefile template specified for framework {}.'.format(framework))
    return makefile


def make_run_command(framework, suite, test_target):
    """
    Creates the command for the framework to run a subset of tests.
    :param framework: The Framework to get the command from
    :param suite: the test suite to run usually $1 in makefile
    :param test_target: path to compiled test file target. ex: tests.dll
    :return: command string
    """
    command = INSTALLED_FRAMEWORKS.get(framework).get('command')
    return command.format(suite=suite, test_file=test_target)


def make_command_line_args(framework, file_str, recursive, glob_pattern):
    """
    Creates command line arguments to be given to
    the parser in the makefile.
    :param arguments: arguments from optparse
    :return: string of command line arguments for python call in makefile
    """
    command_line = "--framework {} -f {} -p {}"
    if recursive:
        command_line += " -r"
    return command_line.format(framework, file_str, glob_pattern)


def makefile_generator(arguments):
    """

    :param arguments: the arguments object created by argparse
    :return: a filled in Makefile template string
    """
    run_test_command = make_run_command(arguments.framework, '$1', arguments.test_target)
    cmd_line = make_command_line_args(arguments.framework, arguments.files,
                                      arguments.recursive, arguments.pattern)

    entry_point = 'ecparse'
    list_cmd = '{} {}'.format(entry_point, cmd_line)
    makefile_string = get_makefile(arguments)
    return makefile_string.format(testrunner=arguments.test_runner, list_cmd=list_cmd, run_cmd=run_test_command)


def main():
    arguments = parser.parse_args()
    makefile_string = makefile_generator(arguments)
    with open(arguments.makefile_path, 'w') as makefile:
        makefile.write(makefile_string)
    print makefile_string

if __name__ == '__main__':
    main()