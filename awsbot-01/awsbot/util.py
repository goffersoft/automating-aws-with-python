#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Utility functions."""

import datetime
from uuid import uuid4
import csv
import mimetypes
import json
from json.decoder import JSONDecodeError
import hashlib
from pathlib import Path
import html5lib
from html5lib.html5parser import ParseError


def get_file_as_string(filename):
    """Get the contents of a file as a string."""
    try:
        fname, err = get_file_path(filename)
        if not err:
            filename = fname
        with open(filename) as file:
            return file.read(), None
    except FileNotFoundError as file_error:
        return None, str(file_error)


def is_valid_html_file(html_file):
    """Validate the contents of the file as html.

    raises the FileNotFoundException
    """
    fname, err = get_file_path(html_file)
    if not err:
        html_file = fname
    with open(html_file) as file:
        try:
            parser = html5lib.HTMLParser(strict=True)
            parser.parse(file)

            return True, None
        except ParseError as parse_error:
            return False, str(parse_error)


def is_valid_html_string(html_string):
    """Validate the string passed in as html."""
    try:
        parser = html5lib.HTMLParser(strict=True)
        parser.parse(html_string)

        return True, None
    except ParseError as parse_error:
        return False, str(parse_error)


def is_valid_json_file(json_file):
    """Validate the contents of the file as json.

    raises the FileNotFoundException
    """
    fname, err = get_file_path(json_file)
    if not err:
        json_file = fname
    with open(json_file) as file:
        try:
            json.load(file)
            return True, None
        except JSONDecodeError as decode_error:
            return False, str(decode_error)


def is_valid_json_string(json_str):
    """Validate the string passed in as json."""
    try:
        json.loads(json_str)
        return True, None
    except JSONDecodeError as decode_error:
        return False, str(decode_error)


def is_valid_html(html_content, file_type=None, estr=None):
    """Validate the filename or a string passed in as html."""
    try:
        if file_type is None or file_type == 'file':
            aok, err = is_valid_html_file(html_content)
        else:
            aok, err = is_valid_html_string(html_content)

        if aok:
            return True, 'file' if file_type is None else file_type, None

        if estr is None:
            return False, None, f'Invalid Json String: {err}'

        return False, None,\
            f'Invalid file name or html string: str([{estr}, {err}])'
    except FileNotFoundError as file_error:
        return is_valid_html(html_content, 'str', str(file_error))


def is_valid_json(json_content, file_type=None, estr=None):
    """Validate the filename or a string passed in as json."""
    try:
        if file_type is None or file_type == 'file':
            aok, err = is_valid_json_file(json_content)
        else:
            aok, err = is_valid_json_string(json_content)

        if aok:
            return True, 'file' if file_type is None else file_type, None

        if estr is None:
            return False, None, 'Invalid Json String:' + err

        return False, None,\
            f'Invalid file name or json string: str([{estr}, {err}])'
    except FileNotFoundError as file_error:
        return is_valid_json(json_content, 'str', str(file_error))


def walk_fs_tree(path,
                 pfunc=lambda p, root:
                 print(f'{str(p)} : ' +
                       f'{str(p.relative_to(root).as_posix())}'),
                 ignore_hidden_files=True,
                 root=None):
    """Walk and process files in fs tree.

    walk fs specified by Path object and executes pfunc
    for each file found in path
    """
    if root is None:
        root = path

    for node in path.iterdir():
        if node.is_dir():
            walk_fs_tree(node, pfunc, ignore_hidden_files, root)
        elif node.is_file():
            if ignore_hidden_files and node.parts[-1].startswith('.'):
                continue
            pfunc(node, root)


def get_content_type_from_filename(filename):
    """Get mime type from file name."""
    content_type, _ = mimetypes.guess_type(filename)
    content_type =\
        'text/plain' if not content_type else content_type

    return content_type


def csv_to_dict(csvfilename, outputdict, dictvalue_type):
    """Initialize dictionary from the csvfile.

    'output_dict' is a dictionary
    'dictvalue_type' is the type associated with dict value
    """
    try:
        fname, err = get_file_path(csvfilename)
        if not err:
            csvfilename = fname

        with open(csvfilename) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                outputdict[row[0]] = dictvalue_type(*row[1:len(row)])

            return True, None
    except FileNotFoundError as file_err:
        return False, str(file_err)


def md5digest(filename, chunksize=None):
    """Compute the md5digest in hex of the contents of 'filename'.

    if chunksize is None or the file size <= chunk size
    then the md5 digest is computed on the entire file

    if filesize is > chunksize
    then the md5digest is computed for each individual chunk
    of the file. These digests are then appended together
    and an digest of digests is computed and returned.
    the number of chunks is appended to the returned digest
    """
    try:
        md5s = []
        fname, err = get_file_path(filename)
        if not err:
            filename = fname
        with open(filename, 'rb') as file:
            while True:
                if chunksize is None:
                    data = file.read()
                else:
                    data = file.read(chunksize)

                if data:
                    md5s.append(hashlib.md5(data))
                else:
                    break

        if len(md5s) < 1:
            return hashlib.md5().hexdigest(), None

        if len(md5s) == 1:
            return md5s[0].hexdigest(), None

        data = b''.join(md5.digest() for md5 in md5s)
        return '{}-{}'.format(hashlib.md5(data).hexdigest(), len(md5s)), None
    except FileNotFoundError as file_error:
        return None, str(file_error)


def get_file_path(path):
    """Determine if path is within the awsbot directory.

    if input path is valid, return input path
    else
        1) get path of this module
        2) get its parent
        3) concatenate parent with 'path'
        4) if valid path, return this new path
    """
    node = Path(path).expanduser().resolve()
    if node.exists():
        return path, None

    node = Path(__file__).parent.joinpath(path)

    if node.exists():
        return str(node), None

    return None, f'Invalid path name : {path}'


def does_file_exist(input_filename):
    """Determine if the file exists."""
    path = Path(input_filename).expanduser().resolve()

    if not path.exists():
        return False, None

    if not path.is_file():
        return False, None

    return True, path


def getuuid():
    """Return a randomly generated UUID4 object."""
    return uuid4()


def str_to_list(input_str, valid_values=None, delimiter=',',
                remove_duplicates=False):
    """Convert a string to a list."""
    if not input_str:
        return None, 'Need input_Str to be specified'

    input_list = input_str.split(delimiter)

    if not valid_values:
        return input_list, None

    for item in input_list:
        if item not in valid_values:
            return None, f'{item} not in list of ' + \
                f'supported values : {valid_values}'

    if remove_duplicates:
        input_list, err = remove_duplicates_from_list(input_list)
        if err:
            return None, err

    return input_list, None


def str_to_set(input_str, valid_values=None, delimiter=',',
               remove_duplicates=False):
    """Convert a string to a set."""
    output_list, err = str_to_list(input_str, valid_values,
                                   delimiter, remove_duplicates)

    if not output_list:
        return None, err

    return set(output_list), None


def convert_to_list(values, valid_values=None, delimiter=',',
                    remove_duplicates=False):
    """Convert a string or a list to a list."""
    if not values:
        return None, 'Requre values to convert'

    if isinstance(values, str):
        values, err = str_to_list(values, valid_values, delimiter)
        if err:
            return None, err

    if remove_duplicates:
        values, err = remove_duplicates_from_list(values)
        if err:
            return None, err

    return values, None


def convert_to_set(values, valid_values=None, delimiter=','):
    """Convert a string or a list to a set."""
    values, err = convert_to_list(values, valid_values, delimiter)
    if err:
        return None, err

    return set(values), None


def is_valid_dir_path(path_to_dir):
    """Determine if the input dir path is valid.

    if its valid, return a path object
    """
    path = Path(path_to_dir).expanduser().resolve()

    if path.is_dir():
        return True, path

    return False, None


def is_valid_file_path(path_to_file):
    """Determine if the input file path is valid.

    if its valid, return a path object
    """
    path = Path(path_to_file).expanduser().resolve()

    if path.is_dir():
        return False, None

    if path.is_file():
        return True, path

    if path.parent.is_dir():
        return True, path

    return False, None


def get_utcnow_with_tzinfo():
    """Get utc datetime string with tzinfo."""
    return datetime.datetime.utcnow().astimezone().isoformat()


def str_range_to_int(str_range, min_lo=0, max_hi=65535,
                     delimiter='-', wildcard='any'):
    """Get range specified as <from>-<to> as tuple of ints."""
    if not str_range:
        return False, None, None

    try:
        parts = str_range.split(delimiter)

        if len(parts) > 2:
            return False, None, None

        if len(parts) == 1 and parts[0] == wildcard:
            lo_val = min_lo
            hi_val = max_hi
        elif len(parts) == 1:
            lo_val = int(parts[0])
            hi_val = lo_val
        elif parts[0] == wildcard and parts[1] == wildcard:
            lo_val = min_lo
            hi_val = max_hi
        elif parts[0] == wildcard:
            lo_val = min_lo
            hi_val = int(parts[1])
        elif parts[1] == wildcard:
            lo_val = int(parts[0])
            hi_val = max_hi
        else:
            lo_val = int(parts[0])
            hi_val = int(parts[1])

        if hi_val < lo_val:
            return False, None, None

        if hi_val > max_hi:
            return False, None, None

        if lo_val < min_lo:
            return False, None, None

        return True, lo_val, hi_val
    except (AttributeError, ValueError):
        return False, None, None


def validate_range(lo_val, hi_val, min_lo=0, max_hi=65535):
    """Validate Range."""
    try:
        if lo_val and isinstance(lo_val, str):
            lo_val = int(lo_val)

        if lo_val and lo_val < min_lo:
            return False, None, None

        if hi_val and isinstance(hi_val, str):
            hi_val = int(hi_val)

        if hi_val and hi_val > max_hi:
            return False, None, None

        if lo_val and hi_val and hi_val < lo_val:
            return False, None, None

        return True, lo_val, hi_val
    except (AttributeError, ValueError):
        return False, None, None


def remove_duplicates_from_list(input_list):
    """Remove duplicates, Preserves ordering."""
    if not input_list:
        return None, 'Need input_list to be specified'
    input_set = set(input_list)
    output_list = []
    for item in input_list:
        if item in input_set:
            output_list.append(item)

    return output_list, None


def get_dict_from_list(keys, values, def_value_func,
                       remove_duplicates=False,
                       valid_values=None, delimiter=','):
    """Create a dict from lists of keys and values.

    keys list must be specified.
    if not enough values, the supplied function
    will be called to get a value.
    """
    if not keys:
        return None, 'Need Keys to be specified'

    key_list = None
    value_list = None
    key_value_dict = None

    key_list, err = convert_to_list(keys, valid_values,
                                    delimiter, remove_duplicates)
    if err:
        return None, err

    if values:
        value_list, err = convert_to_list(values, valid_values,
                                          delimiter, remove_duplicates)
        if err:
            return None, err

    key_value_dict = {key: value_list[index]
                      if value_list and index < len(value_list)
                      else def_value_func(key, value_list)
                      for index, key in enumerate(key_list)}

    return key_value_dict, None


if __name__ == '__main__':
    pass
