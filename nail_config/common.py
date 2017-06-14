def is_del_key(dct: dict, key: str):
    return len(key) > 1 and key[0] == '-' and dct[key] is None


def dict_update(result: dict, dict2: dict, nochange=True, callback=None):
    if callback is None:
        callback = dict_update
    for key in dict2:
        if is_del_key(dict2, key):
            del_key = key[1:]
            if del_key in result:
                del result[del_key]
    if nochange:
        for key in dict2:
            if is_del_key(dict2, key):
                continue
            if key in result:
                if type(dict2[key]) == dict:
                    if type(result[key]) == dict:
                        result[key] = callback(result[key], dict2[key], nochange)
                if type(dict2[key]) == list and type(result[key]) == list:
                    for item in dict2[key]:
                        if item not in result[key]:
                            result[key] += [item]
            else:
                result[key] = dict2[key]
    else:
        for key in dict2:
            if is_del_key(dict2, key):
                continue
            if type(dict2[key]) == dict:
                if key not in result or type(result[key]) != dict:
                    result[key] = {}
                result[key] = callback(result[key], dict2[key], nochange)
            elif type(dict2[key]) == list:
                if key not in result or type(result[key]) != list:
                    result[key] = []
                for item in dict2[key]:
                    if item not in result[key]:
                        result[key] += [item]
            else:
                result[key] = dict2[key]
    return result


def dict_glue(dict1: dict, dict2: dict, nochange=True):
    result = dict1.copy()
    dict_update(result, dict2, nochange=nochange, callback=dict_glue)
    return result


def add_to_dict(dct, path, value, delimiter='/'):
    keys = path.split(delimiter)
    d = dct
    for key in keys[:-1]:
        if key not in d or d[key] is None:
            d[key] = {}
        d = d[key]
        if type(d) != dict:
            return False
    d[keys[-1]] = value
    return True

if __name__ == "__main__":
    import sys

    if 'test' in sys.argv:
        import doctest

        doctest.testmod(verbose=True)
