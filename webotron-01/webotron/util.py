import json
import html5lib
import mimetypes
from json.decoder import JSONDecodeError
from html5lib.html5parser import ParseError
from pathlib import Path


def get_file_as_string(filename):
    """  get the contents of a file as a string.
         raises the FileNotFoundException
    """

    try:
        with open(filename) as file:
            return file.read(), None
    except FileNotFoundError as e:
        return None, str(e)


def is_valid_html_file(html_file):
    """  validates the contents of the file as html
         raises the FileNotFoundException
    """
    with open(html_file) as file:
        try:
            parser = html5lib.HTMLParser(strict=True)
            parser.parse(file)

            return True, None
        except ParseError as e:
            return False, str(e)


def is_valid_html_string(html_string):
    """ validates the string passed in as html """

    try:
        parser = html5lib.HTMLParser(strict=True)
        parser.parse(html_string)

        return True, None
    except ParseError as e:
        return False, str(e)


def is_valid_json_file(json_file):
    """  validates the contents of the file as json
         raises the FileNotFoundException
    """

    with open(json_file) as file:
        try:
            json.load(file)
            return True, None
        except JSONDecodeError as e:
            return False, str(e)


def is_valid_json_string(json_str):
    """ validates the string passed in as json """

    try:
        json.loads(json_str)
        return True, None
    except JSONDecodeError as e:
        return False, str(e)


def is_valid_html(html, type=None, estr=None):
    """ validates the filename or a string passed in as html """

    try:
        if type is None or type == 'file':
            ok, err = is_valid_html_file(html)
        else:
            ok, err = is_valid_html_string(html)

        if ok:
            return True, 'file' if type is None else type, None

        if estr is None:
            return False, None, f'Invalid Json String: {err}'
        else:
            return False, None,\
                f'Invalid file name or html string: str([{estr}, {err}])'
    except FileNotFoundError as e:
        return is_valid_html(html, 'str', str(e))


def is_valid_json(json, type=None, estr=None):
    """ validates the filename or a string passed in as json """

    try:
        if type is None or type == 'file':
            ok, err = is_valid_json_file(json)
        else:
            ok, err = is_valid_json_string(json)

        if ok:
            return True, 'file' if type is None else type, None

        if estr is None:
            return False, None, 'Invalid Json String:' + err
        else:
            return False, None,\
                f'Invalid file name or json string: str([{estr}, {err}])'
    except FileNotFoundError as e:
        return is_valid_json(json, 'str', str(e))


def walk_fs_tree(path,
                 pfunc=lambda p, root: print(f'{str(p.absolute())} : ' +
                                             f'{str(p.relative_to(root))}'),
                 ignore_hidden_files=True,
                 root=None):
    """walk and process files in fs tree

         walk fs specified by Path object and executes pfunc
         for each file found in path
    """

    if root is None:
        root = path

    for p in path.iterdir():
        if p.is_dir():
            walk_fs_tree(p, pfunc, ignore_hidden_files, root)
        elif p.is_file() and not p.parts[-1].startswith('.'):
            pfunc(p, root)


def get_content_type_from_filename(filename):
    """ get mime type from file name """

    content_type, _ = mimetypes.guess_type(filename)
    content_type =\
        'text/plain' if not content_type else content_type

    return content_type

if __name__ == '__main__':
    passd
