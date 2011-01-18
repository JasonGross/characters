#!/usr/bin/python
def format_for_matlab(object_):
    if object_ is None:
        return 'NaN'
    if isinstance(object_, int):
        return 'int32(' + str(object_) + ')'
    if isinstance(object_, str):
        return "'" + object_.replace("'", "''").replace('\n', '\\n') + "'"
    if isinstance(object_, list):
        return '{' + ', '.join(map(format_for_matlab, object_)) + '}'
    return str(object_)
