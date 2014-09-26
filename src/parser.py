from parse_tools import print_test_names
from argparse import ArgumentParser
from settings import get_component
from fnmatch import fnmatch
import os

argparser = ArgumentParser()

argparser.add_argument("--framework", dest="framework", required=True,
                    help="Which framework to parse.")


argparser.add_argument("--files", "-f", action="store", dest="files", default=os.getcwd(),
                    help="A directory or comma separated list of files to search")

argparser.add_argument("--pattern", "-p", action="store", dest="pattern",
                    help="glob pattern for files to search", default='*')

argparser.add_argument("--recursive", "-r", action="store_true", dest="recursive",
                        help="Whether to recursively search directory", default=False)

argparser.add_argument("--agent", "-a", action="store", default=0, dest="agents", type=int,
                    help="How many agents are you using")



def full_filenames(root, file_lst):
    """
    Creates a list of full file paths from
    the output of os.listdir

    :param root: the root of the files
    :param file_lst: list of file names
    :return: a list of the root joined to all the files
    """
    return [os.path.join(root, fn) for fn in file_lst]


def list_directory_files(directory, recursive, glob_pattern):
    """
    Lists the all of the file names in a directory

    :param directory: directory to search
    :param recursive: whether to recursively search directory
    :param glob_pattern: pattern to match files to. defaults to all files
    :return: a list of full path file names
    """
    if recursive:
        all_files = []
        for root, dirs, files in os.walk(directory):
            all_files += full_filenames(root, files)

    else:
        full_names = full_filenames(directory, os.listdir(directory))
        all_files = [fn for fn in full_names if os.path.isfile(fn)]

    relevant_files = filter(lambda filename: fnmatch(filename, glob_pattern), all_files)
    return relevant_files


def get_input_files(file_str, recursive, glob_pattern):
    """
    Takes a comma delimited string of files and directories and returns a list
    of file names.

    :param file_str: comma delimited string of files and dirs
    :param recursive: bool to look recursively thru directories
    :param glob_pattern: the pattern to match files to
    :return: list of filenames
    """
    input_fn = file_str.split(',')
    file_names = []

    for fn in input_fn:
        if os.path.isdir(fn):
            file_names += list_directory_files(fn, recursive, glob_pattern)
        else:
            file_names += [fn]
    return file_names

def testfile_parse(arguments):
    """
    Using the argparse arguments calls print_test_names
    :param arguments: argparse arguments
    :return: None
    """
    framework = arguments.framework
    nodes = get_component(framework, 'nodes')
    strip = get_component(framework, 'strip')
    full_name = get_component(framework, 'full_name')
    files = get_input_files(arguments.files, arguments.recursive, arguments.pattern)
    print_test_names(files, nodes, full_name, strip, agents=arguments.agents)


def main():
    arguments = argparser.parse_args()
    testfile_parse(arguments)

if __name__ == '__main__':
    main()
