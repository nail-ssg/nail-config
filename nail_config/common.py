def dict_concat(dict1, dict2):
    """
    Существующие значения изменяются
    Не существующие добавляются
    >>> d = {'a':{'b':'c'}, 'd':['e','f'], 'g':'f'}
    >>> dict_concat(d, {'a':{'b':'cc', 'i':'j'}, 'd':['e','h'], 'g':'ff'})
    >>> d == {'a': {'b': 'cc', 'i': 'j'}, 'd': ['e', 'f', 'h'], 'g': 'ff'}
    True
    """
    for key in dict2:
        if type(dict2[key]) == dict:
            if key not in dict1 or type(dict1[key]) != dict:
                dict1[key] = {}
            dict_concat(dict1[key], dict2[key])
        elif type(dict2[key]) == list:
            if key not in dict1 or type(dict1[key]) != list:
                dict1[key] = []
            for item in dict2[key]:
                if item not in dict1[key]:
                    dict1[key] += [item]
        else:
            dict1[key] = dict2[key]


def dict_concat2(dict1, dict2):
    result = dict1.copy()
    dict_concat(result, dict2)
    return result


def dict_enrich(dict1: dict, dict2: dict):
    """
    Существующие значения НЕ изменяются
    Не существующие добавляются
    >>> dict_enrich({'a':{'b':'c'}, 'd':['e','f'], 'g':'f'}, {'a':{'b':'cc', 'i':'j'}, 'd':['e','h'], 'g':'ff'}) == {'a':{'b':'c', 'i':'j'}, 'd':['e','f','h'], 'g':'f'}
    True
    """
    result = dict1.copy()
    for key in dict2:
        if key in result:
            if type(dict2[key]) == dict:
                if type(result[key]) == dict:
                    result[key] = dict_enrich(result[key], dict2[key])
            if type(dict2[key]) == list and type(result[key]) == list:
                for item in dict2[key]:
                    if item not in result[key]:
                        result[key] += [item]
        else:
            result[key] = dict2[key]
    return result


if __name__ == "__main__":
    import sys

    if 'test' in sys.argv:
        import doctest

        doctest.testmod(verbose=True)
