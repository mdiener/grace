from builtins import str
import os
import sys
import json
import collections
from future.types.newstr import newstr


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def get_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def load_json(string):
    obj = {}

    try:
        obj = json.loads(string)
    except ValueError as e:
        raise e

    if sys.version_info.major < 3:
        return _json_decode(obj)

    # if sys.version_info.major < 3:
    #     d = _json_decode(obj)
    #     if 'dizmo_settings' in d:
    #         print(isinstance(d['dizmo_settings']['display_name'], str))
    #         print(isinstance(d['dizmo_settings']['display_name'], unicode))
    #         print(type(d['dizmo_settings']['display_name']))
    #     return d

    return obj


def write_json(string):
    try:
        return json.dumps(string)
    except:
        raise


def _json_decode_list(data):
    decoded = []

    for item in data:
        if isinstance(item, unicode):
            item = str(item)
        elif isinstance(item, list):
            item = _json_decode_list(item)
        elif isinstance(item, dict):
            item = _json_decode_dict(item)
        decoded.append(item)

    return decoded


def _json_decode_dict(data):
    decoded = {}

    for key, value in data.items():
        if isinstance(key, unicode):
            key = str(key)

        if isinstance(value, unicode):
            value = str(value)
        elif isinstance(value, dict):
            value = _json_decode_dict(value)
        elif isinstance(value, list):
            value = _json_decode_list(value)

        decoded[key] = value

    return decoded


def _json_decode(data):
    if isinstance(data, list):
        return _json_decode_list(data)
    elif isinstance(data, dict):
        return _json_decode_dict(data)
    elif isinstance(data, unicode):
        return str(data)
    else:
        return data


def isstring(string):
    if isinstance(string, str):
        return True

    if sys.version_info.major < 3:
        if isinstance(string, newstr):
            return True
        if isinstance(string, basestring):
            return True

    return False
