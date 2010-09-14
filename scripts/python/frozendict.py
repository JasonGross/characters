class FrozenDict(dict):
    """
    A FrozenDict is an immutable dictionary.
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__hash = None
        self.__init__ = None

    __delitem__ = None
    __setitem__ = None
    clear = None

    def copy(self):
        return type(self)(dict.copy(self))
    pop = None
    popitem = None
    setdefault = None
    update = None
    def __hash__(self):
        if self.__hash is None:
            self.__hash = hash(tuple([(key, self[key]) for key in sorted(self.keys())]))
        return self.__hash

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, dict.__repr__(self))

    @classmethod
    def fromkeys(S, v=None):
        """
        FrozenDict.fromkeys(S[,v]) -> New FrozenDict with keys from S and values equal to v.
        v defaults to None.
        """
        return FrozenDict(dict.fromkeys(S, v))
    
         
