#!/usr/bin/python
_INT = {}
_INT[8] = [-128, 127]
_INT[16] = [-32768, 32767]
_INT[32] = [-2147483648, 2147483647]
_INT[64] = [-9223372036854775808, 9223372036854775807]
_UINT64_MAX = 18446744073709551615

def format_for_matlab(object_):
    if object_ is None:
        return 'NaN'
    if isinstance(object_, bool):
        return str(object_).lower()
    if isinstance(object_, int):
        for i in sorted(_INT.keys()):
            if _INT[i][0] <= object_ <= _INT[i][1]:
                return 'int%d(%d)' % (i, object_)
        if 0 <= object_ and object_ <= _UINT64_MAX:
            return 'uint64(%d)' % object_
        return "'%d'" % object_
    if isinstance(object_, str):
        return "'" + object_.replace("'", "''").replace('\n', '\\n') + "'"
    if isinstance(object_, list):
        return '{' + ', '.join(map(format_for_matlab, object_)) + '}'
    return str(object_)
