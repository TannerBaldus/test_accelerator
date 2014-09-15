
from fnmatch import fnmatch
import os
import re


def full_filenames(root, file_lst):
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


def get_node_match(node, line_number, lines, strip):
    do_strip = lambda text, flag: text.strip() if flag else text
    line = do_strip(lines[line_number], strip)
    initial_match = node['initial'](line)

    if initial_match and node.get('after'):
        if line_number+1 >= len(lines):
            return None
        next_line = do_strip(lines[line_number+1], strip)
        return node['after'](next_line)
    return initial_match



def node_search(search_files, node_lst, strip=True):
    """
    Iterates through each file looking for matches
    defined in a framework's node list.

    :param search_files:
    :param node_lst:
    :param strip:
    :return:
    """

    max_depth = len(node_lst)-1
    node_lst.sort(key=lambda node: node['depth'])
    running_name = '{}'

    for fn in search_files:
        cur_depth = 0
        with open(fn) as search_file:
            lines = search_file.readlines()
            for line_number,line in enumerate(lines):

                cur_node = node_lst[cur_depth]
                line = line.strip()

                node_match = get_node_match(cur_node, line_number, lines, strip)

                if node_match:
                    cur_name = node_match

                else:
                    match = None
                    for index in range(cur_depth):
                        match = get_node_match(node_lst[index], line_number, lines, strip)

                        if match:
                            cur_depth = index
                            cur_name = match
                            break

                    if not match:
                        continue

                if cur_depth == max_depth:
                    yield '{}.{}'.format(running_name, cur_name)

                else:
                    if cur_depth == 0:
                        running_name = node_match
                    else:
                        running_name = '{}.{}'.format(running_name, cur_name)

                    cur_depth = (cur_depth+1) % len(node_lst)



def print_test_names(agents, file_str, recursive, glob_pattern, node_list, strip, delimiter=','):
    input_fn = file_str.split(',')
    file_names = []
    for fn in input_fn:
        if os.path.isdir(fn):
            file_names += list_directory_files(file_str, recursive, glob_pattern)
        else:
            file_names += fn

    names = [name for name in node_search(file_names, node_list, strip)]
    length = len(names)
    chunk_len = length/agents

    for i in range(1, agents+1):
        next = i*chunk_len
        if i == agents:
            next = max(length, next)
        print delimiter.join(names[i-1:next])


