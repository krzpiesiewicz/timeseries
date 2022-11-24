
def init_if_none(var, constructor=None, value=None, **constructor_params):
    assert (constructor is None) ^ (value is None)
    if var is None:
        if constructor is not None:
            var = constructor(**constructor_params)
        else:
            var = value
    return var
