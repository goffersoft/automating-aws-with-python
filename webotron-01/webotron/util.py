#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Utility functions."""

import csv
import mimetypes
import json
from json.decoder import JSONDecodeError
import hashlib
from pathlib import Path
import html5lib
from html5lib.html5parser import ParseError


def get_file_as_string(filename):
    """Get the contents of a file as a string.

    raises the FileNotFoundException
    """
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
            ok, err = is_valid_html_file(html_content)
        else:
            ok, err = is_valid_html_string(html_content)

        if ok:
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
            ok, err = is_valid_json_file(json_content)
        else:
            ok, err = is_valid_json_string(json_content)

        if ok:
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
        elif node.is_file() and not node.parts[-1].startswith('.'):
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
    """Determine if path is within the webotron directory.

    if input path is valid, return input path
    else
        1) get path of this module
        2) get its parent
        3) concatenate parent with 'path'
        4) if valid path, return this new path
    """
    node = Path(path)
    if node.exists():
        return path, None

    node = Path(__file__).parent.joinpath(path)

    if node.exists():
        return str(node), None

    return None, f'Invalid path name : {path}'


if __name__ == '__main__':
    pass
