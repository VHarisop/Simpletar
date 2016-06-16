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

import os, subprocess

"""
simpletar.lib -- Contains most utility methods needed for simpletar.
"""

# set of commonly used suffixes for archive files
SUFFIXES = {
        'bzip2': ('.bz2', '.bz', '.bzip2'),
        'gzip': ('.gz', '.gzip'),
        'tar': ('.tar',),
        'xz': ('.xz',)
}

# set of magic bytes found in headers of associated archive files
MAGIC = {
        'xz': b'\xFD\x37\x7A\x58\x5A\00',
        'gzip': b'\x1F\x8B\x08',
        'bzip2': b'\x42\x5A\x68',
        'tar': b'\x75\x73\x74\x61\x72'
}


def get_type_by_ext(filename):
    """
    Matches a file extension against a list of known extensions to
    determinge the archive type that it associates with.

    Parameters
    ----------
    filename : str
        The name of the archive file.

    Returns
    -------
    str
        The associated archive type.
    """
    # isolate the extension
    ext = os.path.splitext(filename)[-1]
    assoc = [k for k, v in SUFFIXES.items() if ext in v]

    error_msg = (
            'Unrecognized file extension. '
            'Please specify one of: {.gz, .gzip} for gzip files, '
            '{.bz, .bzip, .bzip2} for bzip2 files, .xz for XZ files '
            'or .tar for simple tar files')

    if not assoc:
        raise ValueError(error_msg)
    else:
        return assoc.pop()


def is_tar_file(filename):
    """
    Reads a file's magic number to determine if it is a plain .tar file
    or not, returning a boolean that indicates it.

    Parameters
    ----------
    filename : str
        The name of the archive file.

    Returns
    -------
    bool
        A boolean indicating if the file is a plain .tar archive or not.

    Raises
    ------
    ValueError
        If the filename argument points to a file that does not exists.
    """
    try:
        with open(filename, 'rb') as f:
            f.read(257) # TAR files's magic numbers have an offset of 257
            return f.read(len(MAGIC['tar'])) == MAGIC['tar']
    except FileNotFoundError:
        raise ValueError("File %s not found" % filename)


def get_type_by_header(filename):
    """
    Reads a file's header and tries to match it against a set of known
    magic numbers to determine what type of archive it is, if any.

    Parameters
    ----------
    filename : str
        The name of the (potential) archive file.

    Returns
    -------
    str
        A string containing the archive type, empty otherwise.

    Raises
    ------
    ValueError
        If the passed filename points to a file that either does not exist
        or does not conform to one of the acceptable archive formats.
    """
    if is_tar_file(filename):
        return 'tar'
    else:
        max_len = max(len(i) for i in MAGIC.values())
        try:
            with open(filename, 'rb') as f:
                cont = f.read(max_len)
        except FileNotFoundError:
            raise ValueError("File %s not found" % filename)

        # if one of the known magic numbers was found, return it
        for key, magic in MAGIC.items():
            if cont.startswith(magic):
                return key

        # otherwise, raise a relevant ValueError
        raise ValueError('File %s is not a file of either tar, gzip, '
                         'bzip2 or XZ format')

def suffixes(filetype):
    """
    Returns a list of commonly used suffixes for a given filetype,
    or None if it is not a filetype recognized by the application.

    Parameters
    ----------
    filetype : str
        The filetype whose common suffixes are sought.

    Returns
    -------
    iterable str
        A tuple containing commonly used suffixes.
    """
    return SUFFIXES.get(filetype, None)


def list_files(name):
    """
    Lists all the files of an archive file.

    Parameters
    ----------
    name : str
        The name of the archive file.
    """
    subprocess.call(['tar', '--list', '-f', name])


def delete_files(name, *args):
    """
    Delete a set of files from an archive.
    
    Note: file deletion works only with uncompressed archives

    Parameters
    ----------
    name : str
        The name of the archive file to delete from.
    args: iterable str
        A set of files to be deleted
    """
    subprocess.call(['tar', '--delete', '-f', name] + list(args))


def update_files(name, *args):
    """
    Update a set of files in an archive, appending them if their version
    is more recent than the one in the archive.

    Note: file update works only with uncompressed archives

    Parameters
    ----------
    name : str
        The name of the archive file to update files.
    args: iterable str
        A set of files to be added.
    """
    subprocess.call(['tar', '--update', '-f', name] + list(args))


def create_tar_file(name, *args):
    """
    Creates a tar archive using "tar -cvf" from a list of files.

    Parameters
    ----------
    name : str
        The name of the archive file to be created.
    args: iterable str
        A set of files to include in the archive.
    """
    name += ('' if name.endswith(suffixes('tar')) else '.tar')
    subprocess.call(['tar', '-cvf', name] + list(args))


def extract_tar_file(name):
    """
    Untars a tar archive using "tar -xvf".

    Parameters
    ----------
    name : str
        The name of the archive file.
    """
    subprocess.call(['tar', '-xvf', name])


def create_gzip_file(name, *args):
    """
    Creates a tar.gz archive using "tar -cvzf" from a list of files.

    Parameters
    ----------
    name : str
        The name of the archive file to be created.
    args: iterable str
        A set of files to include in the archive.
    """
    name += ('' if name.endswith(suffixes('gzip')) else 'tar.gz')
    subprocess.call(['tar', '-cvzf', name] + list(args))


def extract_gzip_file(name, *args):
    """
    Extracts files from a tar.gz archive using "tar -xvzf".

    Parameters
    ----------
    name : str
        The name of the archive file.
    """
    subprocess.call(['tar', '-xvzf', name])


def create_bzip_file(name, *args):
    """
    Creates a tar.bz2 archive using "tar -cvjf" from a list of files.

    Parameters
    ----------
    name : str
        The name of the archive file to be created.
    args: iterable str
        A set of files to include in the archive.
    """
    name += ('' if name.endswith(suffixes('bzip2')) else '.tar.bz2')
    subprocess.call(['tar', '-cvjf', name] + list(args))


def extract_bzip_file(name, *args):
    """
    Extracts files from a tar.bz2 archive using "tar -xvjf".

    Parameters
    ----------
    name : str
        The name of the archive file.
    """
    subprocess.call(['tar', '-xvjf', name])


def create_xz_file(name, *args):
    """
    Creates a .tar.xz archive using "tar -cvJf".

    Parameters
    ----------
    name : str
        The name of the archive file.
    args: iterable str
        A set of files to include in the archive.
    """
    name += ('' if name.endswith(suffixes('xz')) else '.tar.xz')
    subprocess.call(['tar', '-cvJf', name] + list(args))


def extract_xz_file(name, *args):
    """
    Extracts a .tar.xz archive using "tar -xvJf".

    Parameters
    ----------
    name : str
        The name of the archive file.
    """
    subprocess.call(['tar', '-xvJf', name])
