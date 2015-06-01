import os
import sys
import json
import collections


def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def get_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))


def update(d, u):
    for k, v in u.iteritems():
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

    return _json_decode(obj)


def write_json(string):
    try:
        return json.dumps(string)
    except:
        raise


def _json_decode_list(data):
    decoded = []

    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _json_decode_list(item)
        elif isinstance(item, dict):
            item = _json_decode_dict(item)
        decoded.append(item)

    return decoded


def _json_decode_dict(data):
    decoded = {}

    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')

        if isinstance(value, unicode):
            value = value.encode('utf-8')
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
        return data.encode('utf-8')
    else:
        return data
