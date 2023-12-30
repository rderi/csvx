import csv
from io import StringIO
from expression_parser import ExpressionParser
from values import Formula, Literal
import cell_types as types
from expression_evaluator import eval_expression
import functions
from lark import Tree

class CsvEngine:
    def __init__(self, input):
        self.expression_parser = ExpressionParser()
        self.function_engine = functions.FunctionEngine(functions.standard_fns)
        self.input = StringIO(input)
        self.contents = self._read_csv()
        self._parse_expressions()
        self._assign_literal_types()
        self._eval_expressions()

    def _read_csv(self):
        reader = csv.reader(self.input, skipinitialspace=True, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        return list(reader)

    def _parse_expression(self, cell_value):
        return self.expression_parser.parse(cell_value)

    def _parse_expressions(self):
        for row in self.contents:
            for i, cell in enumerate(row):
                if isinstance(cell, str) and cell.startswith('='):
                    #Meant to fix the error of python's CSV reader ignoring quotes if they are not the first character in a cell.
                    #This is an issue when a cell starts with =" and contains a delimiter, as the delimiter will be treated as regular
                    #Hacky but it works
                    if cell.startswith('="') and len(row) > i + 1 and not row[i + 1].startswith('"') and row[i + 1].endswith('"'):
                        cell = cell + ',' + row[i + 1]
                        row.pop(i + 1)
                    parsed_expression = self._parse_expression(cell[1:])
                    row[i] = Formula(cell[1:], parsed_expression)
    
    def _assign_literal_types(self):
        for row in self.contents:
            for i, cell in enumerate(row):
                if not isinstance(cell, Formula):
                    row[i] = Literal(cell)
            
    def _eval_expressions(self):
        for row in self.contents:
            for i, cell in enumerate(row):
                if isinstance(cell, Formula):
                    parse_tree = cell.parse_tree
                    result = eval_expression(parse_tree, self)
                    cell.set_result(result)

    

    #Converts a1 notation to row and column index
    #E.g., AA3 -> (2, 26)
    def _a1_to_idx(self, a1):
        a1 = a1.upper()
        column = 0
        for i, c in enumerate(a1):
            if c.isalpha():
                column = column * 26 + (ord(c) - ord('A') + 1)
        row = int(''.join(filter(str.isdigit, a1))) - 1
        column -= 1
        return (row, column)
    
    def get_a1(self, a1):
        row, col = self._a1_to_idx(a1)
        return self.get(row, col)

    def get(self, row, col):
        cell = self.contents[row][col]
        if not hasattr(cell, 'value'):
            raise ValueError(f'Cell {row}, {col} has no value yet.')
        return cell.value.value #TODO: fix this messyness




