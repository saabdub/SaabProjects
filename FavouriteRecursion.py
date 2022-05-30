
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


def listfillter(data: list, filteringtype: str) -> list:
    """
        given list can contain multiple type of datatye and return a list of only the type specified
        filteringtype can be one of the following:
            'str','int','float','bool'
    """
    out = []
    if filteringtype == 'str':
        for each in data:
            if isinstance(each, str):
                out.append(each)
    elif filteringtype == 'int':
        for each in data:
            if isinstance(each, int):
                out.append(each)
    elif filteringtype == 'float':
        for each in data:
            if isinstance(each, float):
                out.append(each)
    elif filteringtype == 'bool':
        for each in data:
            if isinstance(each, bool):
                out.append(each)
    else:
        print("Invalid filtering type")
    return out


def recursionlistfillter(data: list, filteringtype: str) -> list:
    """
    same as above but with recursion
    :param data:
    :param filteringtype:
    :return:
    """
    output = []

    if filteringtype.lower() == 'str':
        def string(x: list):
            if isinstance(x[-1], str):
                output.append(x[-1])
                x.pop()
            else:
                x.pop()
            if len(x) > 0:
                string(x)
        string(data)
    elif filteringtype.lower() == 'int':
        def string(x: list):
            if type(x[-1]) is int:
                output.append(x[-1])
                x.pop()
            else:
                x.pop()
            if len(x) > 0:
                string(x)
        string(data)
    elif filteringtype.lower() == 'float':
        def string(x: list):
            if isinstance(x[-1], float):
                output.append(x[-1])
                x.pop()
            else:
                x.pop()
            if len(x) > 0:
                string(x)
        string(data)
    elif filteringtype.lower() == 'bool':
        def string(x: list):
            if isinstance(x[-1], bool):
                output.append(x[-1])
                x.pop()
            else:
                x.pop()
            if len(x) > 0:
                string(x)

        string(data)
    else:
        print("Unsupported Datatype")



    return output
