#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Simpletar.
#
# Simpletar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simpletar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Simpletar.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys

from simpletar.lib import (
    create_tar_file, extract_tar_file, create_gzip_file, extract_gzip_file,
    create_bzip_file, extract_bzip_file, create_xz_file, extract_xz_file,
    suffixes, list_files, delete_files, update_files, get_type_by_header,
    get_type_by_ext
)


def main():
    parser = argparse.ArgumentParser(
        description='A utility that simplifies archive file manipulation '
                    'by trying to determine archive type using filenames '
                    'and/or header "magic bytes".'
    )

    # add a group of mutually exclusive opts:
    # -c, --create : create archive file
    # -x, --extract : extract archive file
    # -l, --list : list archive file contents
    # -d, --delete : delete files from archive
    # -u, --update : update files in archive
    o_group = parser.add_argument_group('Operation')
    op_group = o_group.add_mutually_exclusive_group()

    # create option
    op_group.add_argument(
            '--create', '-c',
            help='Create an archive file',
            action='store_true')

    # extract option
    op_group.add_argument(
            '--extract', '-x',
            help='Extract contents from an archive file',
            action='store_true')

    # list option
    op_group.add_argument(
            '--list', '-l',
            help='List the contents of an archive file',
            action='store_true')

    # delete option
    op_group.add_argument(
            '--delete', '-d',
            help='Delete files from an archive file',
            action='store_true')

    # update option
    op_group.add_argument(
            '--update', '-u',
            help='Update files in an archive file',
            action='store_true')

    # Argument for list of files, separated by whitespace
    parser.add_argument(
            '-f', '--files',
            help='A list of file names',
            nargs='*',
            type=str)

    # add file argument for the archive
    parser.add_argument(
            'archive',
            help='The name of the archive file',
            type=str,
            nargs=1)

    # parse all arguments
    args = vars(parser.parse_args())

    # retrieve archive name and filenames
    archive_name = args['archive'][0]
    files = args['files']

    if args['create']:
        # try to determine file type by filename if the user
        # has opted to create an archive
        try:
            filetype = get_type_by_ext(archive_name)
        except ValueError as e:
            sys.stderr.write('simpletar: ' + e.args[0] + '\n')
            sys.exit(1)
    elif args['update'] or args['delete'] or args['extract']:
        # otherwise, try to determine file type by its
        # header's magic bytes
        try:
            filetype = get_type_by_header(archive_name)
        except ValueError as e:
            sys.stderr.write('simpletar: ' + e.args[0] + '\n')
            sys.exit(1)

        # inform the user that updates and deletions are only
        # allowed with simple .tar files
        if (args['update'] or args['delete']) and filetype != 'tar':
            sys.stderr.write('simpletar: Updating or deleting files in '
                             'archives is not supported for compressed '
                             'file formats.\n')
            sys.exit(1)

    # dictionary for create/extract differences
    func_dict = {
        'tar': (create_tar_file, extract_tar_file),
        'gzip': (create_gzip_file, extract_gzip_file),
        'bzip2': (create_bzip_file, extract_bzip_file),
        'xz': (create_xz_file, extract_xz_file)
    }

    files = args['files']

    if args['list']:
        list_files(archive_name)
    else:
        # check if required arguments are supplied
        if (not files) and (not args['extract']):
            sys.stderr.write('simpletar: no files specified, exiting...\n')
            sys.exit(1)

        # perform appropriate commands
        if args['update']:
            update_files(archive_name, *files)
        elif args['delete']:
            delete_files(archive_name, *files)
        elif args['create']:
            func_dict[filetype][0](archive_name, *files)
        elif args['extract']:
            func_dict[filetype][1](archive_name)
