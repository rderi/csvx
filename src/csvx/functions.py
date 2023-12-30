import cell_types as types

def _inc(x):
    if len(x) != 1:
        raise ValueError('Expected single cell as argument')
    arg = x[0]
    if not isinstance(arg, types.Number):
        raise ValueError('Expected number')
    
    arg.value += 1
    return arg

def _dec(x):
    if len(x) != 1:
        raise ValueError('Expected single cell as argument')
    arg = x[0]
    if not isinstance(arg, types.Number):
        raise ValueError('Expected number')
    
    arg.value -= 1
    return arg

def _sum(x):
    if len(x) != 1:
        raise ValueError('Expected single argument') #Todo: maybe add multipe arguments?
    arg = x[0]
    if not isinstance(arg, types.List):
        raise ValueError('Expected list')
    if not all(isinstance(item, types.Number) for item in arg.value):
        raise ValueError('Expected list of numbers')
    return types.Number(sum(item.value for item in arg.value))


standard_fns = {
    'inc': _inc,
    'dec': _dec,
    'sum': _sum
}

class FunctionEngine():
    def __init__(self, functions):
        self.functions = functions
    
    def call_fn(self, function_name, args):
        if function_name not in self.functions:
            raise ValueError(f'Function {function_name} not found')
        return self.functions[function_name](args)