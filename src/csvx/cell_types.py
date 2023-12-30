class Value():
    def __init__(self, value):
        self.value = value 
    
    def __str__(self):
        return f'{self.value}'

class Text(Value):
    def __init__(self, value):

        #TODO: avoid hardcoding quote type, here and elsewhere
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]

        super().__init__(value)

    
class Number(Value):
    def __init__(self, value):
        try:
            value = float(value)
            super().__init__(value)
        except ValueError:
            raise ValueError(f'Expected number, got {value}')

class Logical(Value):
    def __init__(self, value):
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        else:
            raise ValueError(f'Expected boolean, got {value}')
        super().__init__(value)

def detect_literal_type(value):
    try:
        return Number(value)
    except ValueError:
        pass
    try:
        return Logical(value)
    except ValueError:
        pass
    return Text(value)