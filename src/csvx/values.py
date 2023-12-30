import cell_types as types

class Cell:
    def __init__(self, value):
        
        if not isinstance(value, types.Value):
            raise ValueError('type must be a subclass of Value')
        else:
            self.value = value

    def __str__(self):
        return str(self.value)
    
class Formula(Cell):
    def __init__(self, formula, parse_tree):
        self.formula = formula #store raw formula for error reporting etc.
        self.parse_tree = parse_tree

    
    def set_result(self, result):
        self.value = types.detect_literal_type(result)
    
    def __str__(self):
        if hasattr(self, 'value'):
            return f'{self.formula} = {self.value}'
        else:
            return f'{self.formula} = [NOT EVALUATED]'

class Literal(Cell):
    def __init__(self, literal):
        super().__init__(types.detect_literal_type(literal))
    def __str__ (self):
        return str(self.value)
    