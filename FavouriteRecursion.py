
"""
    Deep nested Json Flattening.
    Badly designed surveys or exams

"""

"""
    Create a dictionary from a deeply nested Json, making it 1 level deep
    Returns a dictionary if and only if the input is NOT a empty dictionary.
    
"""
def flattening(nested_json: dict, sep: str = '.') -> dict:

    out = dict()

    def flat(x: (list, dict, str), name: str = ''):
        if type(x) is dict:
            if x.__len__() > 0:
                for each in x:
                    flat(x[each], f'{name}{each}{sep}')
            else:
                out[name[:-1]] = ""
        elif type(x) is list:
            i = 0
            if len(x) > 0:
                for each in x:
                    if not all(isinstance(each1, str) or isinstance(each1, int) for each1 in x):
                        flat(each, f'{name}{i}{sep}')
                        i += 1
                    else:
                        out[name[:-1]] = x
            else:
                out[name[:-1]] = ""
                i += 1
        else:
            out[name[:-1]] = x
    if nested_json.__len__() > 0:
        flat(nested_json)
        return out
    else:
        print("Json Cannot be empty")


