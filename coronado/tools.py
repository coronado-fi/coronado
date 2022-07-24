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
        if 'api' in v:
            v = v.replace('api', 'API')
        if 'Bin' in v and v != 'binary' and v != 'binder' and v != 'bind' and v != 'cubing':
            v = v.replace('Bin', 'BIN')
        if v == 'id':
            v = 'objID'
        elif 'Id' in v and 'Ident' not in v and 'Idio' not in v:
            v = v.replace('Id', 'ID')
        # Alphabetical from here; use a lookup table if it gets too big:
        elif v == 'iat':
            v = 'issuedAt'
        elif v == 'iss':
            v = 'issuingServer'
        elif v == 'jti':
            v = 'tokenIssuerID' # acronyms everywhere!
        elif 'mcc' in v or 'Mcc' in v:
            v.replace('mcc', 'MCC')
        elif v == 'mid':
            v = 'aMID'
        elif v == 'sub':
            v = 'subject'
        # TODO: from Matt - fix this for realz next version
        #       Use a library for camelCase <--> snake_case.
        #       Something like stringcase but that can interpret
        #       acronyms.
        elif 'Url' in v and v[0] not in [ 'c', 'h', ]:
            v = v.replace('Url', 'URL')

        keysTable[k] = v

    result = dict()
    for k,v in d.items():
        result[keysTable[k]] = v

    return result

