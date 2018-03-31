#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
    This script will help you in renaming files
    Copyright (C) 2017 MAIBACH ALAIN

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact: alain.maibach@gmail.com / 34 rue appienne, 13480 Calas - FRANCE.
'''

import os
import sys
import re
import unicodedata
import argparse

__author__ = "Alain Maibach"
__status__ = "Released"

PYTHON3 = sys.version_info.major == 3

CURSCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
CURSCRIPTNAME = os.path.splitext(os.path.basename(__file__))[0]


def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def rm_special_char(instr):
    """
    TO Describe
    """
    cleanedStr = re.sub('\W+', '_', instr)
    return(cleanedStr)


def cleanStr(txt, lowerit=False):
    """
    TO Describe
    """
    string = rm_special_char(strip_accents(txt))
    if lowerit:
        string = string.lower()

    return(string)


def files_within(directory_path, regex=".*", exten=False):
    """
    TO Describe
    """
    if exten:
        if isinstance(exten, list):
            nbargs = len(exten)
            if nbargs == 0:
                print("ERROR: Missing extension value")
                exit(1)
            else:
                newexten = ()
                for idx, p in enumerate(exten):
                    newexten = newexten + (p,)
                exten = newexten

        elif exten == "":
            print("ERROR: Missing extension value")
            exit(1)

        for dirpath, dirnames, filenames in os.walk(directory_path):
            files = filter(lambda x: x.endswith(exten), filenames)
            for file_name in files:
                yield os.path.join(dirpath, file_name)

    else:
        if regex != ".*":
            if regex == "*":
                regex = ".*"

        regex = re.compile(regex)
        for dirpath, dirnames, filenames in os.walk(directory_path):
            files = filter(regex.search, filenames)
            for file_name in files:
                yield os.path.join(dirpath, file_name)


def dirs_within(directory_path, regex=".*"):
    """
    """
    regex = re.compile(regex)
    for dirpath, dirnames, filenames in os.walk(directory_path):
        dirs = filter(regex.search, dirnames)
        for dir_name in dirs:
            yield os.path.join(dirpath, dir_name)


def format_dir_name(fulldirname, lowerit=False, regex=False, replace=False):
    """
    """
    dirpath = os.path.dirname(os.path.abspath(fulldirname))
    dirname = os.path.basename(os.path.abspath(fulldirname))

    new_dirname = cleanStr(txt=dirname, lowerit=lowerit)
    replacedname = new_dirname

    if regex:
        replacedname = re.sub(
            pattern=regex,
            repl='',
            string=dirname,
            flags=re.IGNORECASE)

    if replace:
        nbargsfound = len(replace)
        if nbargsfound != 2:
            if nbargsfound == 1:
                print("ERROR: Bad use of 'transform' only one arg found: {}.\nMake sure to protect it with quotes. Ignoring transform operation ..".format(replace))
            elif nbargsfound > 2:
                print("ERROR: Bad use of 'transform' more than two args found: {}.\nMake sure to protect it with quotes. Ignoring transform operation: ..".format(replace))
        else:
            replacedname = re.sub(
                pattern=replace[0],
                repl=replace[1],
                string=dirname,
                flags=re.IGNORECASE)

    if replacedname != dirname:
        finalname = "{}/{}".format(dirpath, replacedname)
        finalname = os.path.normpath(finalname)
        finalname = os.path.normcase(finalname)
    else:
        finalname = fulldirname

    return(finalname)


def format_file_name(fullname, lowerit=False, regex=False, replace=False):
    """
    """
    dirpath = os.path.dirname(os.path.abspath(fullname))
    filename = os.path.basename(os.path.abspath(fullname))
    splited = os.path.splitext(filename)
    exten = splited[1]
    name = splited[0]

    new_name = cleanStr(txt=name, lowerit=lowerit)
    replacedname = new_name

    if regex:
        replacedname = re.sub(
            pattern=regex,
            repl='',
            string=new_name,
            flags=re.IGNORECASE)

    if replace:
        nbargsfound = len(replace)
        if nbargsfound != 2:
            if nbargsfound == 1:
                print("ERROR: Bad use of 'transform' only one arg found: {}.\nMake sure to protect it with quotes. Ignoring transform operation ..".format(replace))
            elif nbargsfound > 2:
                print("ERROR: Bad use of 'transform' more than two args found: {}.\nMake sure to protect it with quotes. Ignoring transform operation: ..".format(replace))
        else:
            replacedname = re.sub(
                pattern=replace[0],
                repl=replace[1],
                string=new_name,
                flags=re.IGNORECASE)

    if replacedname != name:
        finalname = "{}/{}{}".format(dirpath, replacedname, exten)
        finalname = os.path.normpath(finalname)
        finalname = os.path.normcase(finalname)
    else:
        finalname = fullname

    return(finalname)


def move_res(src, dst, verbose=False):
    try:
        os.rename(src, dst)
    except PermissionError as err:
        print("ERROR: Permission error, unable to rename {} to {}".format(src, dst))
        return(False)
    except FileNotFoundError as err:
        print("ERROR: File not found, unable to rename {} to {}".format(src, dst))
        return(False)
    else:
        print('INFO: Resource {} renamed into {}'.format(src, dst))
        return(True)


def delete_res(resource):
    try:
        os.remove(resource)
    except OSError as err:
        print('ERROR: '.format(err['strerror']))
        return(False)
    else:
        print('INFO: Resource {} removed'.format(resource))
        return(True)


def argCommandline():
    """
    Manage cli script args
    """
    parser = argparse.ArgumentParser(
        description='Rename files removing non ascii chars')
    parser.add_argument(
        "-d",
        "--dir",
        action="store",
        dest="dir",
        help=u"Indicate that you will rename a whole directory of files",
        metavar='/path/to/dir/',
        required=False,
        default=False)
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="file",
        type=str,
        help=u"Indicate that you will rename only one file",
        metavar='/path/to/file',
        required=False,
        default=False)
    parser.add_argument(
        "-r",
        "--rem-regex",
        action='store',
        dest='regex',
        help=u"Extended regex str to remove while renaming file(s)",
        metavar='.*toto_fc$',
        required=False,
        default=False)
    parser.add_argument(
        "-t",
        "--transform",
        action='store',
        dest='overegex',
        help=u"Extended regex str to replace while renaming file(s)",
        nargs='*',
        metavar='"_{2,}" "_"',
        required=False,
        default=False)
    parser.add_argument(
        "-e",
        "--del-file-ext",
        action='store',
        dest='extens',
        nargs='*',
        help=u"Used only with -d option, allow you to remove files with extensions defined here.",
        metavar='.txt .html',
        required=False,
        default=False)
    parser.add_argument(
        "-i",
        "--lower-case",
        action='store_true',
        dest='tolower',
        help=u"Use this to force renaming to lower case",
        required=False)
    parser.add_argument(
        "-s",
        "--supess-files",
        action='store',
        dest='file2del',
        help=u"Used only with -d option, allow you to remove files with name matching the regex.",
        metavar='^_DS.*$',
        required=False,
        default=False)
    parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        dest='verbose',
        help=u"Print verbose informations.",
        required=False)

    args = parser.parse_args()
    if len(sys.argv) <= 1:
        parser.print_help()
        exit(1)

    result = vars(args)
    return(result)


if __name__ == "__main__":
    """
      Bash Tests:
      ----------
        mkdir -p "test 1/toto___/Ha ba/what ?"
        touch "test 1/toto___/Ha ba/what ?/oO@é-y.txt"
        touch "test 1/toto___/Ha ba/what ?/oO@ô é-y-2.txt"
        touch "test 1/toto___/Ha ba/what ?/muzik mon gars.mp3"
        touch "test 1/toto___/Ha ba/what ?/muzik mon gars.mkv"
        touch "test 1/toto___/Ha ba/what ?/muzik mon -tout peti gars.zip"
        touch "test 1/toto___/Ha ba/what ?/haha.jpg"
        touch "test 1/[ Torrent9.tv ] Annabelle.2.Creation.2017.FRENCH.BDRip.XviD-GZR.avi"
        tree

        # File test
        rename-files -f "[ blablablh ] coucou.2.Creation.2017.FRENCH.BDRip.XviD-GZR.avi"

        # directories tests

        # formating dir and files only
        rename-files -d "./test 1"
        tree

        # lowering all
        rename-files -d "./test_1" -i
        tree

        # replacing expression in name
        rename-files -d "./test_1" --transform "_{2,}" "_"
        tree

        # removing files from exten list
        rename-files -d "./test_1" --del-file-ext .txt
        tree

        rename-files -d "./test_1" --del-file-ext .mp3 .mkv
        tree

        # removing file from regex
        rename-files -d "./test_1" --supess-files ^muzik.*gars
        tree

        # formating removing regex
        rename-files -d "./test_1" --rem-regex ^ha_
        tree

        rm test_1/ -r

        mkdir -p "test 1/toto/Ha ba/what ?"
        touch "test 1/toto/Ha ba/what ?/oO@é-y.txt"
        touch "test 1/toto/Ha ba/what ?/oO@ô é-y-2.txt"
        touch "test 1/toto/Ha ba/what ?/muzik mon gars.mp3"
        touch "test 1/toto/Ha ba/what ?/muzik mon gars.mkv"
        touch "test 1/toto/Ha ba/what ?/muzik mon -tout peti gars.zip"
        touch "test 1/toto/Ha ba/what ?/haha.jpg"
        tree

        rename-files -d "./test 1" --rem-regex ^ha_ --del-file-ext .mp3 .mkv --supess-files ^muzik.*gars -i
    """

    args = argCommandline()

    if args['dir']:
        path = str(args['dir'])

        if os.path.isdir(args['dir']):
            # renaming all sub-directories
            dirlst = []

            dir_list = list(dirs_within(directory_path=path))
            while len(dir_list) > 0:
                for directory in dir_list:
                    origdir = directory
                    newdir = format_dir_name(
                        fulldirname=directory,
                        lowerit=args['tolower'],
                        regex=args['regex'],
                        replace=args['overegex'])
                    if origdir != newdir:
                        dirlst.append({origdir: newdir})
                        directory = newdir
                    dir_list = list(dirs_within(directory_path=directory))

            # reversing list before renaming to avoid not found errors
            reversedlst = list(reversed(dirlst))

            if PYTHON3:
                for d in reversedlst:
                    for origin, dest in d.items():
                        move_res(src=origin, dst=dest, verbose=args['verbose'])
            else:
                for d in reversedlst:
                    for origin, dest in d.items():
                        move_res(src=origin, dst=dest, verbose=args['verbose'])

            # renaming main directory
            mainewdir = format_dir_name(
                fulldirname=path,
                lowerit=args['tolower'],
                regex=args['regex'],
                replace=args['overegex'])
            if path != mainewdir:
                move_res(src=path, dst=mainewdir, verbose=args['verbose'])
                exit(1)

            # removing files with exten defined in args['extens'] in main
            # directory renamed
            if args['extens']:
                filesfound = list(
                    files_within(
                        directory_path=mainewdir,
                        exten=args['extens']))
                for f in filesfound:
                    if not delete_res(resource=f):
                        print("ERROR: Unable to remove {}".format(f))

            # removing file matchin regex defined in args['file2del'] in main
            # directory renamed
            if args['file2del']:
                filesfound = list(
                    files_within(
                        directory_path=mainewdir,
                        regex=args['file2del']))
                for f in filesfound:
                    if not delete_res(resource=f):
                        print("ERROR: Unable to remove {}".format(f))

            # Now renaming all files found recursively in main directory
            # renamed
            file_list = list(files_within(directory_path=mainewdir))
            for f in file_list:
                origpath = f
                newpath = format_file_name(
                    fullname=f,
                    lowerit=args['tolower'],
                    regex=args['regex'],
                    replace=args['overegex'])
                if origpath != newpath:
                    move_res(
                        src=origpath,
                        dst=newpath,
                        verbose=args['verbose'])
        else:
            print('ERROR: Directory {} not found'.format(args['dir']))

    elif args['file']:
        origpath = str(args['file'])
        newpath = format_file_name(
            fullname=origpath,
            lowerit=args['tolower'],
            regex=args['regex'],
            replace=args['overegex'])
        if origpath != newpath:
            move_res(src=origpath, dst=newpath, verbose=args['verbose'])
