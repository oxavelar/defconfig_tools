#!/usr/bin/env python3
#
# This will analyze the defconf and explore in the kernel specified
# folder to see if it is being used. This is useful to keep clean defconfig
# files between projects.
#
# author: oxavelar

import sys
import os
import re
import gzip
import itertools



def read_files(*args):
    """
    Recieves paths of files to open, with or without gzip.
    And returns two file descriptor objects.
    """
    fd_files = list()

    for file in args:
        if (file.find('.gz') != -1):
            fd_files.append(gzip.open(file, 'rb'))
        else:
            fd_files.append(open(file, 'rb'))
    
    return fd_files


def find_in_source_code(search_path, string):
    """
    Will look starting from the path recursively for any ocurrences, depending
    on the criteria but returning true means that there is significant code
    using the searched string in the current directory.
    """
    print(search_path)
    return True


def defconfig_analyze(defconfig_file):
    """
    Used to analyze a defconfig, and assuming the file lives inside
    the kernel code to be checked for utilization, it returns a tuple
    of items that are indeed used, or what could have been deprecated
    """
    active = deprecated = list()

    # Guesses the source code path by defconfig name
    ksrc_path = os.path.abspath(defconfig_file.name)
    ksrc_path = os.path.abspath(os.path.join(ksrc_path, '../../../..'))

    # Starts processing the defconfig to look for patterns
    pattern = re.compile(r'(CONFIG_)([a-zA-Z0-9_]*).*')

    for line in defconfig_file:
        # Multiple match is allowed by using chain method on itertools
        match_iter = itertools.chain(re.finditer(pattern, str(line)), )
        
        for match in match_iter:
            
            # The #define name is extracted from the search
            name = re.search(pattern, str(line)).group(2)
            print(name)
    
            # If not used anywhere in the sourcecode, mark as deprecated
            find_in_source_code(ksrc_path, name)
    
    return active, deprecated


def main(argv=sys.argv):
    
    if (len(sys.argv) != 2):
        print('ERROR: Usage of the script is:\n %s defconfig\n' % (os.path.basename(sys.argv[0])))
        exit(-2)
    else:
        # Opens the files for processing
        try:
            defconfig_file, = read_files(sys.argv[1])
        except:
            print('ERROR: Some of the input files were missing, check again!\n')
            exit(-2)
        
        # Do the analysis here
        active, deprecated = defconfig_analyze(defconfig_file)
        
        defconfig_file.close()


if __name__ == '__main__':
    main()
