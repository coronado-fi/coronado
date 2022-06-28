# vim: set fileencoding=utf-8:


# *** constants ***

_VOWELS = ('A', 'E', 'I', 'O', )  # U not included by design


# *** functions ***

def camelCaseOf(aString: str) -> str:
    """
    Form a camelCase symbol from a string.

    Arguments:
    aString - an arbitrary alphanumeric string to be converted

    Returns:
    A camelCase representation of aString
    """
    aString = aString.strip().replace('_', ' ').replace('/', ' ').replace('.', ' ')
    elements = aString.split(' ')
    if len(elements) > 1:
        # Handles acronymx in the middle of the name, Smalltalk rules
        cleanStr = ''
        for element in elements:
            v = element if element.isupper() else element.title()
            if v == 'Mid':
                v = 'MID'
            cleanStr = ' '.join([cleanStr, v])
        cleanStr = cleanStr.strip().replace(' ', '')
        if elements[0].isupper():
            # Handles acronymx, Smalltalk rules
            prefix = 'an' if elements[0][0] in _VOWELS else 'a'
            cleanStr = ''.join([prefix, cleanStr])
    else:
        cleanStr = aString

    if cleanStr.isupper():
        # Handles acronymx, Smalltalk rules
        prefix = 'an' if cleanStr[0] in _VOWELS else 'a'
        result = ''.join([prefix, cleanStr])
    else:
        symbol = list(cleanStr)
        symbol[0] = symbol[0].lower()
        result = ''.join(symbol)

    return result


def tripleKeysToCamelCase(d: dict):
    keysTable = dict()

    for k in d.keys():
        v = camelCaseOf(k)
        if v == 'id':
            v = 'objID'
        elif 'Id' in v and 'Ident' not in v and 'Idio' not in v:
            v = v.replace('Id', 'ID')
        elif v == 'mid':
            v = 'aMID'

        keysTable[k] = v

    result = dict()
    for k,v in d.items():
        result[keysTable[k]] = v

    return result

